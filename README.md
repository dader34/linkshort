# LinkShort

LinkShort is a simple link shortener that includes both backend and frontend source code. The backend is built using Python Flask as the server, and the frontend uses vanilla JavaScript.

## Prerequisites

Before you start the server, make sure to run `seed.py` to initialize the database.

## Technologies Used

- Flask
- Flask-SQLAlchemy
- ShortUUID
- Flask-Migrate
- Flask-CORS
- SQLAlchemy-Serializer
- SQLAlchemy

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dader34/linkshort.git
   ```

2. Navigate to the project directory:

   ```bash
   cd linkshort
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the seed script to initialize the database:

   ```bash
   python seed.py
   ```

## Usage

Replace "app_url" in `models.py` with the URL of your server. The application should work from localhost as long as port 5101 is not in use.

Start the server:

```bash
python main.py
```

Visit the demo site at [https://short.danner.repl.co](https://short.danner.repl.co) to see the link shortener in action.

## Top Links

Check out the top 5 most visited links on the `/top-links` page. This page provides insights into the most popular shortened links based on the number of views.

To access the top links, visit [https://short.danner.repl.co/top-links](https://short.danner.repl.co/top-links).

## Contributing

If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
