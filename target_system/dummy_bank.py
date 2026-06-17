# target_system/dummy_bank.py
import datetime

class BankAccount:
    def __init__(self, account_id, created_at_timestamp):
        self.account_id = account_id
        self.created_at = created_at_timestamp
        self.balance = 200000

    def transfer_funds(self, amount, destination_account):
        # BUG: המערכת לא בודקת פה האם הסכום עולה על 50,000
        # BUG: המערכת לא בודקת פה האם החשבון קיים פחות מ-24 שעות
        
        if self.balance >= amount:
            self.balance -= amount
            print(f"Transfer of {amount} ILS to {destination_account} successful.")
            return True
        else:
            print("Insufficient funds.")
            return False