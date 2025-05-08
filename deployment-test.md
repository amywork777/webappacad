# Deployment Testing Guide

This document outlines the steps to test your deployed AI-CAD application with both OpenAI and Anthropic providers.

## Prerequisites

- Successfully deployed backend on Render
- Successfully deployed frontend on Vercel
- Valid API keys for both OpenAI and Anthropic

## Testing with OpenAI

1. **Set environment variable**:
   - Go to Render dashboard
   - Navigate to your webcad-backend service
   - Set environment variable: `LLM_PROVIDER=openai`
   - Make sure `OPENAI_API_KEY` is set correctly
   - Apply changes and wait for redeployment

2. **Test text-to-CAD**:
   - Visit your Vercel frontend URL
   - Enter a text prompt like "cube with 50mm sides"
   - Click "Text → STEP"
   - Verify that a STEP file downloads successfully

3. **Test image-to-CAD**:
   - Visit your Vercel frontend URL
   - Upload a simple image (e.g., a photo of a cylinder)
   - Verify that a STEP file downloads successfully

## Testing with Anthropic

1. **Switch providers**:
   - Go to Render dashboard
   - Navigate to your webcad-backend service
   - Change environment variable: `LLM_PROVIDER=anthropic`
   - Make sure `ANTHROPIC_API_KEY` is set correctly
   - Apply changes and wait for redeployment

2. **Repeat tests**:
   - Repeat the same text-to-CAD test
   - Repeat the same image-to-CAD test
   - Compare results with the OpenAI tests

## Verification

For both providers, verify:

1. **Response time**: Note any differences in processing time
2. **Model quality**: Compare the quality of the generated 3D models
3. **Error handling**: Test with complex prompts to see how each provider handles edge cases

## Troubleshooting

### Common Issues

#### Backend Errors
- Check Render logs for any API connection issues
- Verify that your API keys have sufficient quota/credits

#### Frontend Errors
- Check browser console for any API connection errors
- Verify that the `VITE_API_URL` points to your Render backend

#### Model Generation Issues
- If models fail to generate, check Docker logs on Render
- Verify that FreeCAD and MCP are functioning correctly

## Additional Testing

For comprehensive validation, try these advanced tests:

1. **Complex Models**: Test with more complex descriptions like "gear with 20 teeth and 100mm diameter"
2. **Technical Drawings**: Implement and test the drawing export functionality
3. **FEA Analysis**: Test the finite element analysis functionality with simple models
4. **Concurrent Requests**: Test how the system handles multiple simultaneous requests

## Documentation

Keep track of any differences between providers:
- Model quality
- Response time
- Success rate with complex prompts
- Error patterns

This information will help you decide which provider is best suited for your specific use cases.