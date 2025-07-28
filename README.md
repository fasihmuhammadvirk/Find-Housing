# Housing Monitor with Flask Web Server

A robust Python script that monitors the STWDO housing portal for new offers and sends email alerts when available. Now includes a Flask web server for deployment on Replit, PythonAnywhere, and monitoring with UptimeRobot.

## Features

- ✅ Monitors housing offers every 30 seconds
- ✅ Sends email alerts when new offers are found
- ✅ Flask web server for deployment and monitoring
- ✅ Comprehensive error handling and logging
- ✅ Prevents duplicate notifications
- ✅ Robust network handling with timeouts
- ✅ Detailed logging to both console and file
- ✅ Web endpoints for health monitoring
- ✅ Ready for Replit and PythonAnywhere deployment
- ✅ Multiple connection methods for proxy issues

## Web Endpoints

The Flask server provides these endpoints for monitoring:

- **`/`** - Home page with basic status
- **`/health`** - Health check with detailed monitoring stats
- **`/status`** - Comprehensive status information

## Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the script first:**
   ```bash
   python test_script.py
   ```

3. **Run the monitor:**
   ```bash
   python main.py
   ```

4. **Access web interface:**
   - Open browser to `http://localhost:8080`
   - Check health at `http://localhost:8080/health`
   - View status at `http://localhost:8080/status`

### Replit Deployment

1. **Create a new Replit project**
2. **Upload the files:**
   - `main.py`
   - `requirements.txt`
   - `README.md`

3. **Set environment variables in Replit:**
   - Go to "Tools" → "Secrets"
   - Add your email credentials:
     - `EMAIL_SENDER`: Your Gmail address
     - `EMAIL_PASSWORD`: Your Gmail App Password
     - `EMAIL_RECEIVER`: Your email address

4. **Run the project:**
   - Click "Run" in Replit
   - The web server will start automatically

5. **Get your Replit URL:**
   - Your app will be available at: `https://your-repl-name.your-username.repl.co`

### PythonAnywhere Deployment

**Note:** PythonAnywhere has proxy restrictions that may affect external HTTPS connections. Use the PythonAnywhere-specific version.

1. **Upload files to PythonAnywhere:**
   - `main_pythonanywhere.py` (use this instead of main.py)
   - `requirements.txt`
   - `test_connection.py`

2. **Test connectivity first:**
   ```bash
   python test_connection.py
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   export EMAIL_SENDER="your-email@gmail.com"
   export EMAIL_PASSWORD="your-app-password"
   export EMAIL_RECEIVER="your-email@gmail.com"
   ```

5. **Run the monitor:**
   ```bash
   python main_pythonanywhere.py
   ```

6. **For continuous running, use screen:**
   ```bash
   screen -S housing_monitor
   python main_pythonanywhere.py
   # Press Ctrl+A, then D to detach
   ```

### UptimeRobot Configuration

1. **Sign up for UptimeRobot** (free tier available)
2. **Add a new monitor:**
   - Monitor Type: HTTP(s)
   - URL: `https://your-repl-name.your-username.repl.co/health` (for Replit)
   - URL: `http://your-pythonanywhere-url/health` (for PythonAnywhere)
   - Monitoring Interval: 5 minutes
   - Alert Threshold: 1 failure

3. **Set up alerts:**
   - Email notifications when the service goes down
   - Get notified when your housing monitor stops working

## Configuration

### Email Settings
The script uses Gmail SMTP. You need to:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password (not your regular password)
3. Update the credentials in the script or set environment variables:
   ```python
   EMAIL_SENDER = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-app-password"
   EMAIL_RECEIVER = "your-email@gmail.com"
   ```

### Environment Variables (for Replit)
```bash
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECEIVER=your-email@gmail.com
```

### Monitoring Settings
- **Check interval:** 30 seconds (configurable in the script)
- **Web server port:** 8080 (configurable via PORT environment variable)
- **URL:** STWDO housing portal (configurable)
- **Log file:** `housing_monitor.log`

## How It Works

1. **Web Server:** Flask server runs on port 8080 in a separate thread
2. **Monitoring:** The script checks the housing portal every 30 seconds
3. **Detection:** It looks for the "No results" message to determine if offers are available
4. **Alerting:** When offers are found (and no previous alert was sent), it sends an email
5. **Logging:** All activities are logged to both console and `housing_monitor.log`
6. **Health Monitoring:** Web endpoints provide real-time status for UptimeRobot

## Safety Features

- **No crashes:** Comprehensive error handling prevents script failures
- **Duplicate prevention:** Only sends one alert per offer cycle
- **Network resilience:** 30-second timeouts prevent hanging
- **Graceful shutdown:** Handles Ctrl+C properly
- **Detailed logging:** All activities tracked for debugging
- **Web monitoring:** UptimeRobot can detect if the service goes down
- **Thread safety:** Flask server runs independently of monitoring logic
- **Multiple connection methods:** Handles proxy and network restrictions

## Web API Endpoints

### GET /
Returns basic status information:
```json
{
  "status": "online",
  "service": "Housing Monitor",
  "timestamp": "2025-07-27T21:30:00",
  "message": "Housing monitor is running and checking for offers every 30 seconds"
}
```

### GET /health
Returns detailed health information:
```json
{
  "status": "healthy",
  "last_check": "2025-07-27T21:30:00",
  "total_checks": 120,
  "offers_found": 5,
  "emails_sent": 2,
  "last_error": null,
  "is_running": true
}
```

### GET /status
Returns comprehensive status:
```json
{
  "service": "STWDO Housing Monitor",
  "status": "running",
  "monitoring_url": "https://www.stwdo.de/en/living-houses-application/current-housing-offers",
  "check_interval": "30 seconds",
  "last_check": "2025-07-27T21:30:00",
  "total_checks": 120,
  "offers_found": 5,
  "emails_sent": 2,
  "last_error": null,
  "uptime": "24/7 monitoring active"
}
```

## Troubleshooting

### Common Issues

1. **Email authentication failed:**
   - Ensure you're using an App Password, not your regular Gmail password
   - Check that 2-factor authentication is enabled

2. **Website access issues:**
   - Check your internet connection
   - The website might be temporarily down

3. **Flask server not starting:**
   - Check if port 8080 is already in use
   - Ensure Flask is installed: `pip install flask`

4. **Replit deployment issues:**
   - Check the console for error messages
   - Ensure all dependencies are in `requirements.txt`
   - Verify environment variables are set correctly

5. **PythonAnywhere proxy errors:**
   - Use `main_pythonanywhere.py` instead of `main.py`
   - Run `python test_connection.py` to test connectivity
   - PythonAnywhere may block external HTTPS connections
   - Consider using Replit as an alternative

6. **UptimeRobot not detecting the service:**
   - Check that your URL is correct
   - Verify the `/health` endpoint returns a 200 status code
   - Test the URL manually in a browser

### PythonAnywhere Specific Issues

**Proxy Error (403 Forbidden):**
```
HTTPSConnectionPool(host='www.stwdo.de', port=443): Max retries exceeded
(Caused by ProxyError('Unable to connect to proxy', OSError('Tunnel connection failed: 403 Forbidden')))
```

**Solutions:**
1. Use `main_pythonanywhere.py` which has multiple connection methods
2. Run `python test_connection.py` to find a working method
3. If all methods fail, PythonAnywhere may not allow external HTTPS connections
4. Consider using Replit or another hosting service

### Log Files

- **Console output:** Real-time monitoring information
- **housing_monitor.log:** Detailed log file with timestamps

## Running in Background

### On macOS/Linux:
```bash
nohup python main.py > output.log 2>&1 &
```

### Using screen:
```bash
screen -S housing_monitor
python main.py
# Press Ctrl+A, then D to detach
# Use 'screen -r housing_monitor' to reattach
```

### On PythonAnywhere:
```bash
screen -S housing_monitor
python main_pythonanywhere.py
# Press Ctrl+A, then D to detach
```

## Monitoring the Monitor

### Check logs:
```bash
tail -f housing_monitor.log
```

### Check web status:
```bash
curl http://localhost:8080/health
```

### Check if Flask server is running:
```bash
curl http://localhost:8080/
```

## Security Notes

- Keep your email credentials secure
- Use environment variables for sensitive data in production
- The script only reads the housing website, it doesn't submit any data
- All network requests use proper headers and timeouts
- Log files may contain sensitive information (email addresses)

## Support

If you encounter issues:
1. Run `python test_script.py` to diagnose problems
2. For PythonAnywhere: Run `python test_connection.py`
3. Check the log file for error messages
4. Test the web endpoints manually
5. Ensure all dependencies are installed correctly
6. Verify UptimeRobot is monitoring the correct URL

## Deployment Checklist

- [ ] All files uploaded to hosting service
- [ ] Environment variables set correctly
- [ ] Dependencies installed (`requirements.txt`)
- [ ] Connection test passed (`test_connection.py` for PythonAnywhere)
- [ ] Script runs without errors
- [ ] Web endpoints accessible
- [ ] UptimeRobot monitor configured
- [ ] Email alerts working
- [ ] Logs being generated

## File Descriptions

- `main.py` - Standard version for Replit and local use
- `main_pythonanywhere.py` - PythonAnywhere-specific version with proxy handling
- `test_connection.py` - Test script for PythonAnywhere connectivity
- `test_script.py` - Comprehensive testing script
- `requirements.txt` - All necessary dependencies
- `README.md` - This documentation 