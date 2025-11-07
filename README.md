# QR & Barcode Generator Agent for Telex.im

A Python-based AI agent that generates QR codes and barcodes, integrated with Telex.im using the A2A protocol.

## Features

- **QR Code Generation**: Create QR codes for any text, URLs, or data
- **Barcode Generation**: Support for CODE128, EAN13, EAN8, and UPC formats
- **Telex Integration**: Seamless integration with Telex.im platform
- **Proactive Messaging**: Daily QR code tips at 9 AM
- **A2A Protocol**: Full compliance with A2A communication standard
- **Clean Architecture**: SOLID principles with separation of concerns

## Architecture

```
src/
├── controllers/          # MVC Controllers
│   └── agent_controller.py
├── services/            # Business Logic
│   ├── qr_service.py
│   └── barcode_service.py
├── models/              # Data Models
│   └── request_models.py
├── utils/               # Utilities
│   ├── message_parser.py
│   └── telex_client.py
└── main.py              # FastAPI Application
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/tulbadex/telex-barcode-generation
cd telex-barcode-generation
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your Telex configuration
```

4. **Run the agent:**
```bash
python -m src.main
```

## Usage

### Telex Commands

- `qr [text]` - Generate QR code
- `barcode [text]` - Generate barcode
- `qr size:15 [text]` - QR with custom size (1-40)
- `barcode format:ean13 [text]` - Barcode with specific format

### Examples

```
qr https://example.com
barcode 1234567890
qr size:20 Hello World
barcode format:ean13 123456789012
```

### Supported Formats

- **QR Codes**: Standard QR with customizable size
- **Barcodes**: CODE128, EAN13, EAN8, UPC

## API Endpoints

- `POST /api/v1/qr` - Generate QR code
- `POST /api/v1/barcode` - Generate barcode
- `POST /` - Telex A2A endpoint
- `GET /api/v1/health` - Health check

## A2A Protocol Integration

The agent follows the A2A protocol specification:

```json
{
  "text": "Response message",
  "type": "text|image",
  "image": "data:image/png;base64,..."
}
```

## Deployment

### Local Development
```bash
python -m src.main
```

### Production (Docker)
```bash
docker build -t qr-barcode-agent .
docker run -p 8000:8000 qr-barcode-agent
```

### Environment Variables

```env
TELEX_WEBHOOK_URL=https://api.telex.im/webhook
AGENT_NAME=QRBarcodeBot
AGENT_PORT=8000
TELEX_CHANNEL_ID=your-channel-id
DEBUG=False
```

## Design Patterns Used

- **MVC Pattern**: Controllers, Services, Models separation
- **Single Responsibility**: Each class has one purpose
- **Dependency Injection**: Services injected into controllers
- **Factory Pattern**: Barcode format creation
- **Strategy Pattern**: Different barcode formats

## Error Handling

- Input validation with Pydantic models
- Graceful error responses
- Logging for debugging
- File cleanup to prevent storage issues

## Testing

```bash
# Run tests
python -m pytest tests/

# Test specific endpoint
curl -X POST "http://localhost:8000/api/v1/qr" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World", "size": 10}'
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Follow SOLID principles
4. Add tests for new features
5. Submit pull request

## License

MIT License - see LICENSE file for details.