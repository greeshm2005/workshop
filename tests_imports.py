# test_imports.py
print("Testing imports...")

try:
    from database import Database
    print("✅ Database imported")
except Exception as e:
    print(f"❌ Database import failed: {e}")

try:
    from models import BookModel, TransactionModel, MemberModel, AdminModel
    print("✅ Models imported")
except Exception as e:
    print(f"❌ Models import failed: {e}")

try:
    from utils import UIHelper, FineCalculator
    print("✅ Utils imported")
except Exception as e:
    print(f"❌ Utils import failed: {e}")

try:
    from login_screens import LoginScreen
    print("✅ LoginScreen imported")
except Exception as e:
    print(f"❌ LoginScreen import failed: {e}")

try:
    from admin_dashboard import AdminDashboard
    print("✅ AdminDashboard imported")
except Exception as e:
    print(f"❌ AdminDashboard import failed: {e}")

try:
    from user_dashboard import UserDashboard
    print("✅ UserDashboard imported")
except Exception as e:
    print(f"❌ UserDashboard import failed: {e}")

try:
    from analytics_dashboard import AnalyticsDashboard
    print("✅ AnalyticsDashboard imported")
except Exception as e:
    print(f"❌ AnalyticsDashboard import failed: {e}")

print("\nTest complete!")