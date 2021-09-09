import requests
import dates_magic

def lambda_handler(event, context):
    custom_datetime = dates_magic.get_current_datetime()
    response = requests.get('https://www.test.com')
    print(response.text)
    return {
        "custom_current_date": custom_datetime.strftime('%B %d, %Y'),
        "requests result": response.text
    }

if __name__ == '__main__':
    lambda_handler('', '')