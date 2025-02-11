from firstrade import account, order, symbols
from src.config import settings


ft_ss = account.FTSession(
    username=settings.USERNAME, password=settings.PASSWORD, email=settings.EMAIL
)


need_code = ft_ss.login()

if need_code:
    code = input("Enter code: ")
    ft_ss.login_two(code)


ft_accounts = account.FTAccountData(ft_ss)
if len(ft_accounts.account_numbers) < 1:
    raise Exception("No accounts found")



print(ft_accounts.all_accounts)

# Print 1st account number.
print(ft_accounts.account_numbers[0])

# Print ALL accounts market values.
print(ft_accounts.account_balances)