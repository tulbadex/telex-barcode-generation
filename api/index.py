def handler(request):
    import json
    
    if request.method == 'GET':
        if request.path == '/':
            return {
                'statusCode': 200,
                'body': json.dumps({"message": "QR & Barcode Generator Agent", "status": "active"}),
                'headers': {'Content-Type': 'application/json'}
            }
        elif request.path == '/health':
            return {
                'statusCode': 200,
                'body': json.dumps({"status": "healthy"}),
                'headers': {'Content-Type': 'application/json'}
            }
        elif request.path == '/.well-known/agent.json':
            return {
                'statusCode': 200,
                'body': json.dumps({
                    "name": "QR & Barcode Generator",
                    "version": "1.0.0",
                    "skills": [
                        {"name": "generate_qr", "description": "Generate QR codes"},
                        {"name": "generate_barcode", "description": "Generate barcodes"}
                    ]
                }),
                'headers': {'Content-Type': 'application/json'}
            }
    
    return {
        'statusCode': 404,
        'body': json.dumps({"error": "Not found"}),
        'headers': {'Content-Type': 'application/json'}
    }