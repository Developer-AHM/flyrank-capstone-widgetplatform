#!/usr/bin/env bash
set -a; source .env; set +a
BASE=http://localhost:8000

get_token() {
  curl -s -X POST "$SUPABASE_URL/auth/v1/token?grant_type=password" \
    -H "apikey: $SUPABASE_KEY" -H "Content-Type: application/json" \
    -d "{\"email\":\"$1\",\"password\":\"password123\"}" \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])"
}

TOKEN_A=$(get_token freshtest2.user@gmail.com)
TOKEN_B=$(get_token tenantb.capstone@gmail.com)
echo "token lengths A/B: ${#TOKEN_A} ${#TOKEN_B}"

code() { curl -s -o /dev/null -w "%{http_code}" "$@"; }
JSON="Content-Type: application/json"

WID=$(curl -s -X POST $BASE/widgets -H "Authorization: Bearer $TOKEN_A" -H "$JSON" \
  -d '{"type":"contact_form","title":"A widget"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "created widget: $WID"

echo "1 no token            (401): $(code $BASE/widgets)"
echo "2 owner reads         (200): $(code $BASE/widgets/$WID/manage -H "Authorization: Bearer $TOKEN_A")"
echo "3 other tenant reads  (404): $(code $BASE/widgets/$WID/manage -H "Authorization: Bearer $TOKEN_B")"
echo "4 B lists             (200): $(code $BASE/widgets -H "Authorization: Bearer $TOKEN_B")"
echo "  B's list body       ([]) : $(curl -s $BASE/widgets -H "Authorization: Bearer $TOKEN_B")"
echo "5 B updates A's       (404): $(code -X PUT $BASE/widgets/$WID -H "Authorization: Bearer $TOKEN_B" -H "$JSON" -d '{"type":"cta","title":"hacked"}')"
echo "6 B deletes A's       (404): $(code -X DELETE $BASE/widgets/$WID -H "Authorization: Bearer $TOKEN_B")"
echo "7 smuggled owner_id   (422): $(code -X POST $BASE/widgets -H "Authorization: Bearer $TOKEN_A" -H "$JSON" -d '{"type":"contact_form","title":"x","owner_id":"evil"}')"
echo "8 A deletes own       (204): $(code -X DELETE $BASE/widgets/$WID -H "Authorization: Bearer $TOKEN_A")"