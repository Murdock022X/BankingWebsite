from admin.routes import Admin_Tools
from website import create_app

# A script used to carry out processes that should 
# occur at the end of every day.
def main():
	app = create_app()

	with app.app_context():
		Admin_Tools.daily_processes()

	return 1

if __name__ == '__main__':
	main()
