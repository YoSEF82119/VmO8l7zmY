# 代码生成时间: 2025-09-23 15:00:52
import quart
def validate_url(url: str) -> bool:
    """Validates the given URL."""
    try:
        # Use requests library to check if the URL is reachable
        import requests
        response = requests.head(url, timeout=5)
        # Check if the response status code is between 200 and 299
        return 200 <= response.status_code < 300
    except requests.RequestException as e:
        # Log the error or handle as per the application's logging strategy
        print(f"Error while validating URL: {e}")
        return False

app = quart.Quart(__name__)

@app.route('/validate-url', methods=['POST'])
async def validate_url_endpoint():
    """Endpoint to validate a URL."""
    data = await quart.request.get_json()
    if 'url' not in data:
        return quart.jsonify({'error': 'URL parameter is missing'}), 400
    
    result = validate_url(data['url'])
    
    # Return the validation result as JSON
    return quart.jsonify({'is_valid': result})

if __name__ == '__main__':
    app.run()