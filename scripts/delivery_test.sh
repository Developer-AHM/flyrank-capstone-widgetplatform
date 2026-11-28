#!/usr/bin/env bash
set -a; source .env; set +a
BASE=http://localhost:8000
JSON="Content-Type: application/json"

TOKEN=$(curl -s -X POST "$SUPABASE_URL/auth/v1/token?grant_type=password" \
  -H "apikey: $SUPABASE_KEY" -H "$JSON" \
  -d '{"email":"freshtest2.user@gmail.com","password":"password123"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
AUTH="Authorization: Bearer $TOKEN"

WID=$(curl -s -X POST $BASE/widgets -H "$AUTH" -H "$JSON" \
  -d '{"type":"contact_form","title":"Delivery test","fields":[{"name":"email","label":"Email","type":"email","required":true}]}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "widget: $WID"

echo; echo "== 1 snippet (owner)"
curl -s $BASE/widgets/$WID/snippet -H "$AUTH"; echo

echo; echo "== 2 snippet without token (expect 401)"
curl -s -o /dev/null -w "%{http_code}\n" $BASE/widgets/$WID/snippet

echo; echo "== 3 public config headers"
curl -s -D - -o /dev/null $BASE/widgets/$WID/config | grep -i -E "^HTTP|cache-control|etag|access-control"
ETAG=$(curl -s -D - -o /dev/null $BASE/widgets/$WID/config | grep -i '^etag:' | cut -d' ' -f2 | tr -d '\r')
echo "etag: $ETAG"

echo; echo "== 4 config body (must not contain owner_id)"
curl -s $BASE/widgets/$WID/config; echo

echo; echo "== 5 same ETag (expect 304)"
curl -s -o /dev/null -w "%{http_code}\n" $BASE/widgets/$WID/config -H "If-None-Match: $ETAG"

echo; echo "== 6 after an edit, the old ETag no longer matches (expect 200)"
echo "PUT status (expect 200): $(curl -s -o /dev/null -w "%{http_code}" -X PUT $BASE/widgets/$WID -H "$AUTH" -H "$JSON" -d '{"type":"contact_form","title":"Edited"}')"
curl -s -o /dev/null -w "%{http_code}\n" $BASE/widgets/$WID/config -H "If-None-Match: $ETAG"

echo; echo "== 7 unknown widget (expect 404)"
curl -s -o /dev/null -w "%{http_code}\n" $BASE/widgets/w_doesnotexist/config

echo; echo "== 8 bundle headers"
curl -s -D - -o /dev/null $BASE/widget.v1.js | grep -i -E "^HTTP|content-type|cache-control"

curl -s -o /dev/null -X DELETE $BASE/widgets/$WID -H "$AUTH"