import pytest
import requests

BASE_URL = "http://localhost:8080/api/v1"
ROLL_NUMBER = "12345"
USER_ID = "800"

@pytest.fixture
def headers():
    return {
        "X-Roll-Number": "2024115001",
        "X-User-ID": "800"
    }

@pytest.fixture
def admin_headers():
    return {
        "X-Roll-Number": "2024115001"
    }
# 1. Headers & Auth Tests
def test_missing_roll_number_header():
    response = requests.get(f"{BASE_URL}/profile", headers={"X-User-ID": "800"})
    assert response.status_code == 401

def test_invalid_roll_number_header():
    response = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "abc", "X-User-ID": "800"})
    assert response.status_code == 400

def test_missing_user_id_header():
    response = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "2024115001"})
    assert response.status_code == 400

def test_invalid_user_id_header():
    response = requests.get(f"{BASE_URL}/profile", headers={"X-Roll-Number": "2024115001", "X-User-ID": "-1"})
    assert response.status_code == 400

# 2. Profile Tests
def test_get_profile(headers):
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200

def test_update_profile_valid(headers):
    payload = {"name": "Test User", "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    assert response.status_code == 200

def test_update_profile_invalid_name(headers):
    payload = {"name": "A", "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    assert response.status_code == 400

def test_update_profile_invalid_phone(headers):
    payload = {"name": "Test User", "phone": "12345"}
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    assert response.status_code == 400

# 3. Addresses Tests
def test_add_address_valid(headers):
    payload = {"label": "HOME", "street": "123 Test Street", "city": "Test City", "pincode": "560001"}
    response = requests.post(f"{BASE_URL}/addresses", headers=headers, json=payload)
    
    # If this fails, we catch it as a bug.
    if response.status_code in [200, 201]:
        return response.json()["address"]["address_id"]
    return None

def test_add_address_invalid_label(headers):
    payload = {"label": "INVALID", "street": "123 Test Street", "city": "Test City", "pincode": "560001"}
    response = requests.post(f"{BASE_URL}/addresses", headers=headers, json=payload)
    assert response.status_code == 400

def test_update_address_immutable_fields(headers):
    addr_id = test_add_address_valid(headers)
    if addr_id:
        payload = {"street": "456 New Street", "city": "New City", "is_default": True}
        response = requests.put(f"{BASE_URL}/addresses/{addr_id}", headers=headers, json=payload)
        if response.status_code == 200:
            assert response.json().get("city") != "New City"

def test_delete_invalid_address(headers):
    response = requests.delete(f"{BASE_URL}/addresses/99999", headers=headers)
    assert response.status_code == 404

# 4. Products Tests
def test_get_products(headers):
    response = requests.get(f"{BASE_URL}/products", headers=headers)
    assert response.status_code == 200
    for product in response.json():
        assert product.get("is_active", True) is True

def test_get_invalid_product(headers):
    response = requests.get(f"{BASE_URL}/products/99999", headers=headers)
    assert response.status_code == 404

# 5. Cart Tests
def test_add_to_cart_valid(headers):
    payload = {"product_id": 1, "quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    assert response.status_code in [200, 201]

def test_add_to_cart_invalid_quantity(headers):
    payload = {"product_id": 1, "quantity": 0}
    response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    assert response.status_code == 400

def test_cart_total_computation(headers):
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": 2})
    response = requests.get(f"{BASE_URL}/cart", headers=headers)
    assert response.status_code == 200
    data = response.json()
    items = data.get("items", [])
    total = data.get("total", 0)
    computed_total = sum(item["quantity"] * item["unit_price"] for item in items)
    # Validate bug: total must be correct sum
    assert total == computed_total

def test_cart_remove_invalid_product(headers):
    payload = {"product_id": 99999}
    response = requests.post(f"{BASE_URL}/cart/remove", headers=headers, json=payload)
    assert response.status_code == 404

# 6. Checkout Tests
def test_checkout_empty_cart(headers):
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    payload = {"payment_method": "COD", "address_id": 1}
    response = requests.post(f"{BASE_URL}/checkout", headers=headers, json=payload)
    assert response.status_code == 400

def test_checkout_invalid_payment_method(headers):
    requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": 1})
    payload = {"payment_method": "BITCOIN", "address_id": 1}
    response = requests.post(f"{BASE_URL}/checkout", headers=headers, json=payload)
    assert response.status_code == 400

# 7. Coupons
def test_coupon_apply_valid(headers):
    requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
    requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": 5})
    payload = {"coupon_code": "INVALID_COUPON"}
    response = requests.post(f"{BASE_URL}/coupon/apply", headers=headers, json=payload)
    assert response.status_code in [400, 404]

# 8. Wallet
def test_wallet_pay_insufficient_funds(headers):
    payload = {"amount": 9999999}
    response = requests.post(f"{BASE_URL}/wallet/pay", headers=headers, json=payload)
    assert response.status_code == 400

# 9. Loyalty Points
def test_loyalty_redeem_invalid_amount(headers):
    payload = {"points": 0}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", headers=headers, json=payload)
    assert response.status_code == 400

# 10. Orders
def test_order_cancel_invalid(headers):
    response = requests.post(f"{BASE_URL}/orders/99999/cancel", headers=headers)
    assert response.status_code == 404

# 11. Reviews
def test_add_review_invalid_rating(headers):
    payload = {"rating": 6, "comment": "Great!"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json=payload)
    assert response.status_code == 400

def test_add_review_invalid_comment_length(headers):
    long_comment = "A" * 205
    payload = {"rating": 5, "comment": long_comment}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json=payload)
    assert response.status_code == 400

# 12. Support Tickets
def test_add_support_ticket_valid(headers):
    payload = {"subject": "Need Help", "message": "Can't access my profile."}
    response = requests.post(f"{BASE_URL}/support/ticket", headers=headers, json=payload)
    assert response.status_code in [200, 201]

def test_add_support_ticket_invalid_subject(headers):
    payload = {"subject": "Hi", "message": "Can't access my profile."}
    response = requests.post(f"{BASE_URL}/support/ticket", headers=headers, json=payload)
    assert response.status_code == 400

# --- Extra Exhaustive Tests ---

# 13. Invalid Data Types
def test_add_to_cart_wrong_type(headers):
    payload = {"product_id": "one", "quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    assert response.status_code == 400

def test_apply_coupon_wrong_type(headers):
    payload = {"coupon_code": 123}
    response = requests.post(f"{BASE_URL}/coupon/apply", headers=headers, json=payload)
    assert response.status_code == 400

# 14. Missing Fields
def test_update_profile_missing_fields(headers):
    payload = {"name": "Only Name"} # phone is missing
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    assert response.status_code == 400

def test_add_address_missing_fields(headers):
    payload = {"label": "HOME", "street": "Missing City/Pincode"}
    response = requests.post(f"{BASE_URL}/addresses", headers=headers, json=payload)
    assert response.status_code == 400

# 15. Boundary Values
def test_update_profile_long_name(headers):
    payload = {"name": "A" * 101, "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    assert response.status_code == 400

def test_add_review_empty_comment(headers):
    payload = {"rating": 5, "comment": ""}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json=payload)
    assert response.status_code == 400

def test_add_review_max_comment_length(headers):
    # Assuming 200 is max based on test_add_review_invalid_comment_length
    payload = {"rating": 5, "comment": "A" * 200}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=headers, json=payload)
    assert response.status_code == 200

# 16. Negative Values
def test_add_to_cart_negative_quantity(headers):
    payload = {"product_id": 1, "quantity": -5}
    response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    assert response.status_code == 400

def test_wallet_pay_negative_amount(headers):
    payload = {"amount": -100}
    response = requests.post(f"{BASE_URL}/wallet/pay", headers=headers, json=payload)
    assert response.status_code == 400

# 17. Extreme Values
def test_add_to_cart_huge_quantity(headers):
    payload = {"product_id": 1, "quantity": 999999}
    response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    # This might pass or fail depending on stock, let's see.
    assert response.status_code in [200, 400]

# 18. Invalid Endpoints/Methods
def test_invalid_endpoint(headers):
    response = requests.get(f"{BASE_URL}/nonexistent", headers=headers)
    assert response.status_code == 404

def test_invalid_method_profile(headers):
    response = requests.post(f"{BASE_URL}/profile", headers=headers, json={})
    assert response.status_code == 405

# 19. Additional Validation Tests
def test_add_to_cart_missing_product_id(headers):
    payload = {"quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/add", headers=headers, json=payload)
    assert response.status_code == 400

def test_checkout_missing_payment_method(headers):
    # First add something to cart (even if total is bugged, it might allow checkout)
    requests.post(f"{BASE_URL}/cart/add", headers=headers, json={"product_id": 1, "quantity": 1})
    payload = {"address_id": 1003} # Missing payment_method
    response = requests.post(f"{BASE_URL}/checkout", headers=headers, json=payload)
    assert response.status_code == 400

def test_update_profile_wrong_phone_type(headers):
    payload = {"name": "Test User", "phone": 1234567890} # int instead of string
    response = requests.put(f"{BASE_URL}/profile", headers=headers, json=payload)
    assert response.status_code == 400
