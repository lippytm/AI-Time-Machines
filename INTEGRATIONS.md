# Platform Integrations Guide

## Overview

AI-Time-Machines now supports cross-platform connectivity, allowing you to integrate your time-series predictions with popular chatbot platforms, analytics tools, and notebook environments.

## Supported Platforms

### 1. ManyChat
**Type:** Chatbot Platform  
**Use Case:** Send prediction updates to Facebook Messenger chatbots  
**Features:**
- Webhook support for real-time updates
- Custom user fields for prediction data
- Quick reply templates

**Configuration:**
```json
{
  "platform": "manychat",
  "apiKey": "your-manychat-api-key",
  "webhookUrl": "https://manychat.com/api/webhook"
}
```

### 2. BotBuilders
**Type:** Multi-Platform Chatbot Builder  
**Use Case:** Automate prediction notifications across multiple messaging platforms  
**Features:**
- Multi-platform support (SMS, WhatsApp, Telegram, etc.)
- NLP integration
- Automated workflows

**Configuration:**
```json
{
  "platform": "botbuilders",
  "apiKey": "your-botbuilders-api-key",
  "webhookUrl": "https://api.botbuilders.com/webhook"
}
```

### 3. OpenClaw
**Type:** Analytics & Automation Platform  
**Use Case:** Feed predictions into analytics pipelines and automation workflows  
**Features:**
- Advanced analytics
- Data export capabilities
- Automation triggers

**Configuration:**
```json
{
  "platform": "openclaw",
  "apiKey": "your-openclaw-api-key",
  "webhookUrl": "https://openclaw.io/api/events"
}
```

### 4. Moltbook
**Type:** Interactive Notebook Platform  
**Use Case:** Embed predictions in interactive notebooks for analysis and visualization  
**Features:**
- Markdown and code cells
- Python visualization support
- Documentation generation

**Configuration:**
```json
{
  "platform": "moltbook",
  "apiKey": "your-moltbook-api-key",
  "config": {
    "notebookId": "your-notebook-id"
  }
}
```

## API Endpoints

### Integrations Management

#### Get All Integrations
```http
GET /api/integrations
Authorization: Bearer {token}
```

**Query Parameters:**
- `platform` (optional): Filter by platform type
- `isActive` (optional): Filter by active status

#### Create Integration
```http
POST /api/integrations
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "My ManyChat Integration",
  "platform": "manychat",
  "description": "Send predictions to ManyChat bot",
  "apiKey": "your-api-key",
  "webhookUrl": "https://example.com/webhook",
  "config": {}
}
```

#### Test Integration
```http
POST /api/integrations/{id}/test
Authorization: Bearer {token}
```

#### Send Prediction to Integration
```http
POST /api/integrations/{id}/send
Authorization: Bearer {token}
Content-Type: application/json

{
  "predictionId": "uuid-of-prediction"
}
```

### Webhook Endpoint (External Platforms)

#### Receive Webhook
```http
POST /api/integrations/webhooks/{platform}
Content-Type: application/json

{
  "event": "prediction_request",
  "data": {...}
}
```

### Export Predictions

#### Export in Multiple Formats
```http
GET /api/predictions/{id}/export?format={format}
Authorization: Bearer {token}
```

**Supported Formats:**
- `json` - Standard JSON format
- `csv` - Comma-separated values
- `xml` - XML format
- `manychat` - ManyChat-specific format
- `botbuilders` - BotBuilders-specific format
- `openclaw` - OpenClaw analytics format
- `moltbook` - Moltbook notebook format

## Export Format Examples

### CSV Format
```csv
timestamp,value,confidence_lower,confidence_upper
0,42.5,40.2,44.8
1,43.1,40.9,45.3
2,43.7,41.5,45.9
```

### JSON Format
```json
{
  "id": "prediction-uuid",
  "modelId": "model-uuid",
  "horizon": 10,
  "predictions": [42.5, 43.1, 43.7],
  "confidence": {
    "lower": [40.2, 40.9, 41.5],
    "upper": [44.8, 45.3, 45.9]
  },
  "metadata": {
    "createdAt": "2026-02-03T21:00:00Z",
    "userId": "user-uuid"
  }
}
```

### XML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<prediction>
  <id>prediction-uuid</id>
  <modelId>model-uuid</modelId>
  <horizon>10</horizon>
  <predictions>
    <value index="0">42.5</value>
    <value index="1">43.1</value>
  </predictions>
  <confidence>
    <lower>
      <value index="0">40.2</value>
    </lower>
    <upper>
      <value index="0">44.8</value>
    </upper>
  </confidence>
</prediction>
```

### ManyChat Format
```json
{
  "messaging_type": "UPDATE",
  "notification_type": "REGULAR",
  "message": {
    "text": "New prediction available",
    "quick_replies": [
      {
        "content_type": "text",
        "title": "View Details",
        "payload": "PREDICTION_uuid"
      }
    ]
  },
  "custom_user_field": {
    "prediction_id": "uuid",
    "predictions": [42.5, 43.1],
    "horizon": 10
  }
}
```

### Moltbook Format
```json
{
  "cells": [
    {
      "type": "markdown",
      "content": "# Prediction uuid\n\nGenerated on 2026-02-03"
    },
    {
      "type": "code",
      "language": "python",
      "content": "predictions = [42.5, 43.1, 43.7]"
    },
    {
      "type": "code",
      "language": "python",
      "content": "import matplotlib.pyplot as plt\nplt.plot(predictions)\nplt.show()"
    }
  ]
}
```

## Usage Examples

### Setting Up an Integration (Frontend)

1. Navigate to the **Integrations** page
2. Click **+ Add Integration**
3. Fill in the integration details:
   - Name: A descriptive name
   - Platform: Choose from the dropdown
   - API Key: Your platform API key
   - Webhook URL: The endpoint to receive data
4. Click **Create Integration**

### Testing an Integration

1. Go to the Integrations page
2. Find your integration
3. Click the **Test** button
4. Check the response status

### Sending a Prediction

Use the API or extend the frontend to send predictions:

```javascript
const response = await axios.post(
  `/api/integrations/${integrationId}/send`,
  { predictionId: 'your-prediction-id' },
  { headers: { Authorization: `Bearer ${token}` } }
);
```

### Exporting Predictions

```javascript
// Export as CSV
const csvData = await axios.get(
  `/api/predictions/${predictionId}/export?format=csv`,
  { headers: { Authorization: `Bearer ${token}` } }
);

// Export for ManyChat
const manychatData = await axios.get(
  `/api/predictions/${predictionId}/export?format=manychat`,
  { headers: { Authorization: `Bearer ${token}` } }
);
```

## Security Considerations

1. **API Keys**: Store API keys securely. They are stored encrypted in the database.
2. **Webhook Authentication**: Implement signature verification for incoming webhooks.
3. **Rate Limiting**: All endpoints are rate-limited to prevent abuse.
4. **HTTPS**: Always use HTTPS in production for webhook URLs.

## Advanced Features

### Custom Webhook Integration

For platforms not explicitly supported:

```json
{
  "platform": "webhook",
  "name": "Custom Integration",
  "webhookUrl": "https://your-service.com/webhook",
  "config": {
    "method": "POST",
    "headers": {
      "X-Custom-Header": "value"
    }
  }
}
```

### Automation Workflows

Combine integrations with predictions for automated workflows:

1. Train a model
2. Generate predictions
3. Automatically send to ManyChat
4. Notify users via chatbot
5. Export to Moltbook for analysis

## Troubleshooting

### Integration Test Fails

- Verify API key is correct
- Check webhook URL is accessible
- Ensure the platform service is running
- Review integration logs

### Webhook Not Receiving Data

- Verify webhook URL is publicly accessible
- Check firewall rules
- Ensure the endpoint accepts POST requests
- Review webhook payload format

### Export Format Issues

- Ensure prediction data is complete
- Check format parameter spelling
- Verify prediction ID is valid

## Future Enhancements

- [ ] Real-time webhook delivery
- [ ] Retry mechanism for failed webhooks
- [ ] Integration analytics and monitoring
- [ ] OAuth2 support for integrations
- [ ] Batch export capabilities
- [ ] Integration templates
- [ ] Custom format builders

## Support

For questions and issues:
- Open an issue on [GitHub](https://github.com/lippytm/AI-Time-Machines/issues)
- Check [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)
