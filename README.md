# RedditTickerAnalytics

## Getting Started
- Start `TickerAPI.py` to initialize API
- Start `stream.py` to begin the stream that will read wsb data
- Start `dashtest.py` to begin local website that will run dashboard
- Paste URL from `dashtest.py` into local browser, and append '/*Ticker Name*' to URL

## Todo
[] Convert axes to use timestamp instead of delta in seconds from program start
[] Refactor data being exported out from WSB stream to include timestamp
[] Create database of all comments with metadata (ticker name, timestamp of comment, etc.)