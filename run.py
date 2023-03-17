from website import create_app

# Create the app.
app = create_app()

if __name__ == '__main__':
    # Run the app.
    app.run(debug=True)