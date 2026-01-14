# How to Add Screenshots to Documentation

## Quick Guide

### 1. Start the Application

```bash
./start.sh
```

Wait for the message:
```
✅ Server started successfully!
🌐 Open in your browser: http://localhost:7860
```

### 2. Open in Browser

Navigate to: http://localhost:7860

### 3. Interact with the Interface

To capture a good screenshot showing all features:

1. **Ask a question** (e.g., "List all employees in the database")
2. **Wait for response** to appear in chat
3. **Click 👍 or 👎** to show feedback buttons
4. **Check the right sidebar** to see:
   - Connected Servers
   - Learning Stats
   - Features

### 4. Capture Screenshot

**On macOS:**
- Press `Cmd + Shift + 4`
- Drag to select the browser window
- Screenshot saved to Desktop

**On Windows:**
- Press `Windows + Shift + S`
- Select area to capture
- Screenshot copied to clipboard (paste to save)

**On Linux:**
- Press `PrtScn` or use Screenshot tool
- Select window or area

### 5. Save Screenshot

Save the image as:
```
ai-agent-interface.png
```

In this directory:
```
/Users/syedraza/mcp-toolkit/docs/screenshots/
```

### 6. Verify

The screenshot should show:
- ✅ Dark theme interface
- ✅ MCP Server selector dropdown
- ✅ Chat conversation with query and response
- ✅ Thumbs up/down feedback buttons
- ✅ Connected Servers panel (right side)
- ✅ Learning Stats panel (right side)
- ✅ Features list at bottom

### 7. Update Git (Optional)

```bash
git add docs/screenshots/ai-agent-interface.png
git commit -m "docs: Add application screenshot"
git push origin main
```

## Recommended Screenshot Settings

- **Resolution:** 1920x1080 or higher
- **Format:** PNG (best quality)
- **Size:** Keep under 2MB
- **Content:** Full interface with example query/response

## Example Screenshot Content

**Query to use:**
```
List all employees in the database
```

**This will show:**
- Database query capability
- MCP server (postgres) in action
- Response with structured data
- Professional interface

## Troubleshooting

### Issue: Application not starting

**Solution:**
```bash
./stop.sh
./start.sh
```

### Issue: Port 7860 already in use

**Solution:**
```bash
./stop.sh
# Wait 5 seconds
./start.sh
```

### Issue: No data showing in response

**Solution:**
1. Check your `.env` file has correct credentials
2. Verify database connection in server status panel
3. Try a simpler query first

## Alternative: Using Existing Screenshot

If you have the screenshot shared earlier in the conversation, you can use that:

1. Download the image from the conversation
2. Rename it to `ai-agent-interface.png`
3. Place it in `/Users/syedraza/mcp-toolkit/docs/screenshots/`
4. Commit to git

## Result

Once added, the screenshot will appear in:
- [README.md](../../README.md) - Main project page
- [LEARNING_SYSTEM.md](../../LEARNING_SYSTEM.md) - Learning system documentation
- [docs/screenshots/README.md](README.md) - Screenshot documentation

And will be visible on GitHub at:
https://github.com/majidraza1228/mcp-toolkit/blob/main/docs/screenshots/ai-agent-interface.png

---

**Note:** Screenshots help users understand what the application looks like before they install it, making documentation more engaging and informative.
