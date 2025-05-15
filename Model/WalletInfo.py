class WalletInfo:
    def __init__(self, wallet_id, customer_number, cdd_level, wallet_level,
                 mobile_number, email_address, document_id, nationality,
                 dob, customer_status, wallet_status, wallet_balance,
                 first_name, last_name, chinese_full_name):
        self.wallet_id = wallet_id
        self.customer_number = customer_number
        self.cdd_level = cdd_level
        self.wallet_level = wallet_level
        self.mobile_number = mobile_number
        self.email_address = email_address
        self.document_id = document_id
        self.nationality = nationality
        self.dob = dob
        self.customer_status = customer_status
        self.wallet_status = wallet_status
        self.wallet_balance = wallet_balance
        self.first_name = first_name
        self.last_name = last_name
        self.chinese_full_name = chinese_full_name
