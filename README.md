# WebSocket Chat Application

A real-time chat application built with Python WebSockets and asyncio. This application provides a server and a beautiful web interface for real-time messaging with features like public chat, private messaging, and user management.

## Features

- **Real-time messaging** using WebSocket protocol
- **Public chat** - messages visible to all connected users
- **Private messaging** - direct user-to-user communication
- **User management** - track online users and handle connections
- **Beautiful web interface** - modern, responsive design
- **Cloud-ready** - optimized for Railway deployment
- **Cross-platform** - works on Windows, macOS, and Linux

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python server/chat_server.py
   ```

3. **Open the web interface:**
   - Open `web/index.html` in your browser
   - Or serve it with a simple HTTP server:
     ```bash
     cd web
     python -m http.server 8080
     ```
   - Then open `http://localhost:8080`

### Railway Deployment (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect the configuration and deploy

3. **Get your public URL:**
   - Railway will give you a public URL like: `https://your-app-name.railway.app`
   - Your WebSocket URL will be: `wss://your-app-name.railway.app`

4. **Share with friends:**
   - Send them the web interface: `https://your-app-name.railway.app`
   - They can open it in any browser and start chatting!

## Usage

### Web Interface

1. **Open the web interface** in your browser
2. **Enter your username** and click "Join Chat"
3. **Start chatting!** The interface includes:
   - Real-time messaging
   - Private messaging
   - User avatars
   - Typing indicators
   - Mobile-responsive design

### Chat Features

- **Public messages** - visible to all users
- **Private messages** - click the "Private" button to send direct messages
- **User status** - see who's online
- **Real-time updates** - instant message delivery

## Project Structure

```
websocket-chat/
├── server/
│   └── chat_server.py      # Main WebSocket server
├── web/
│   └── index.html          # Beautiful web interface
├── requirements.txt        # Python dependencies
├── railway.json           # Railway deployment config
├── render.yaml            # Render deployment config (alternative)
├── DEPLOYMENT.md          # Detailed deployment guide
└── README.md              # This file
```

## Configuration

### Environment Variables

- `HOST` - Server host (default: 0.0.0.0 for cloud deployment)
- `PORT` - Server port (default: 8766)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

### Server Configuration

The server automatically configures itself for cloud deployment:
- Listens on all interfaces (`0.0.0.0`)
- Uses environment variable `PORT` or defaults to 8766
- Optimized for Railway deployment

## API Reference

### Message Types

#### Client to Server

```json
// Login
{
  "type": "login",
  "username": "alice"
}

// Chat message
{
  "type": "chat",
  "message": "Hello everyone!"
}

// Private message
{
  "type": "private",
  "to": "bob",
  "message": "Hi Bob!"
}

// Typing indicator
{
  "type": "typing",
  "is_typing": true
}
```

#### Server to Client

```json
// Login success
{
  "type": "login_success",
  "username": "alice",
  "message": "Welcome alice!",
  "timestamp": "2024-01-01T12:00:00"
}

// Chat message
{
  "type": "chat",
  "username": "alice",
  "message": "Hello everyone!",
  "timestamp": "2024-01-01T12:00:00"
}

// Private message
{
  "type": "private",
  "from": "alice",
  "message": "Hi Bob!",
  "timestamp": "2024-01-01T12:00:00"
}

// User joined
{
  "type": "user_joined",
  "username": "bob",
  "message": "bob joined the chat",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Troubleshooting

### Common Issues

1. **Connection refused**
   - Ensure server is running on port 8766
   - Check firewall settings
   - Verify Railway deployment is successful

2. **Import errors**
   - Install dependencies: `pip install -r requirements.txt`
   - Activate virtual environment if using one

3. **Web interface not loading**
   - Check browser console for errors
   - Verify WebSocket connection to chat server
   - Ensure Railway deployment completed successfully

### Debug Mode

Enable debug logging by modifying `server/chat_server.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Deployment

### Railway (Recommended)

- **Free tier** available
- **Automatic deployment** from GitHub
- **SSL certificates** included
- **Global CDN** for fast access

### Alternative Platforms

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:
- Render
- Heroku
- DigitalOcean
- AWS/GCP/Azure
- Your own server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
- Check the deployment guide

---

**Ready to deploy?** 🚀

1. Push your code to GitHub
2. Deploy to Railway in 5 minutes
3. Share the URL with friends
4. Start chatting remotely!

Happy chatting! 💬 