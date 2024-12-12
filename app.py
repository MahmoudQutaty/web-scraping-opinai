'''
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
from models import db
from models.agent import Agent
from models.chatbot import Chatbot
from models.message import Message
from models.user import User
from scraping import scrape_website
from chatbot import create_chatbot_response

app = Flask(__name__)
app.config.from_object('config.Config')

# Database Initialization
db.init_app(app)
migrate = Migrate(app, db)

def admin_required(f):
    """Decorator to restrict access to admin routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or not session.get('is_admin'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Plain text comparison
            session['user'] = username
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@admin_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin/agents', methods=['GET', 'POST'])
@admin_required
def agents():
    if request.method == 'POST':
        # Create new agent
        name = request.form.get('name')
        picture_url = request.form.get('picture_url', '')
        prompt = request.form.get('prompt', '')

        if not name or not prompt:
            agents = Agent.query.all()
            return render_template(
                'agents.html',
                agents=agents,
                error="Name and prompt are required fields."
            )

        new_agent = Agent(name=name, picture_url=picture_url, prompt=prompt)
        db.session.add(new_agent)
        db.session.commit()

        return redirect(url_for('embed', agent_id=new_agent.id))

    # GET request: List all agents
    agents = Agent.query.all()
    return render_template('agents.html', agents=agents)

@app.route('/admin/agents/embed', methods=['GET', 'POST'])
@admin_required
def embed():
    agents = Agent.query.all()  # Fetch all agents for selection
    script_tag = None

    if request.method == 'POST':
        agent_id = request.form.get('agent_id')
        website_url = request.form.get('website_url', '').strip()

        selected_agent = Agent.query.get_or_404(agent_id)

        if website_url:
            # Scrape website data and update the agent's prompt
            scraped_data = scrape_website(website_url)
            selected_agent.prompt = scraped_data
            db.session.commit()

        # Generate the embed URL for the chatbot
        script_tag = f"<a href='{url_for('chatbot', agent_id=agent_id)}'>Chatbot for {selected_agent.name}</a>"

    return render_template('embed.html', agents=agents, script_tag=script_tag)


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'user' not in session:
        return redirect(url_for('login'))

    agent_id = request.args.get('agent_id')
    agent = Agent.query.get_or_404(agent_id)
    response = None

    if request.method == 'POST':
        try:
            data = request.get_json()
            user_message = data.get('user_message', '')

            # Generate chatbot response
            response = create_chatbot_response(agent.prompt, user_message)

            # Save the interaction to the database
            new_message = Message(
                user_ip=request.remote_addr,
                message=user_message,
                response=response,
                chatbot_id=agent_id
            )
            db.session.add(new_message)
            db.session.commit()

            # Return JSON response
            return {"response": response}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Log the error for debugging
            return {"error": "Failed to process the message"}, 500

    return render_template('chatbot.html', agent=agent)

@app.route('/admin/messages', methods=['GET'])
@admin_required
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
'''

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
from models import db
from models.agent import Agent
from models.chatbot import Chatbot
from models.message import Message
from models.user import User
from scraping import scrape_website
from chatbot import create_chatbot_response

app = Flask(__name__)
app.config.from_object('config.Config')

# Database Initialization
db.init_app(app)
migrate = Migrate(app, db)

def login_required(f):
    """Decorator to restrict access to logged-in users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not email or not password:
            return render_template('signup.html', error="Email and password are required.")
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match.")
        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error="Email is already registered.")

        # Create new user
        new_user = User(email=email, password=password)  # Note: Use hashing in production
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error="Email and password are required.")
        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Plain text comparison (consider hashing for production)
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', error="Invalid credentials.")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)
    return render_template('dashboard.html', user=user)

@app.route('/agents', methods=['GET', 'POST'])
@login_required
def agents():
    user_id = session['user_id']
    if request.method == 'POST':
        # Fetch form inputs
        name = request.form.get('name')
        image_url = request.form.get('image_url', '')
        prompt = request.form.get('prompt', '')

        # Validate input
        if not name :
            agents = Agent.query.filter_by(user_id=user_id).all()
            return render_template(
                'agents.html',
                agents=agents,
                error="Name and prompt are required fields."
            )

        # Create new agent without chatbot
        new_agent = Agent(
            name=name,
            image_url=image_url,
            prompt=prompt,
            user_id=user_id,
            chatbot_id=None  # No chatbot linked initially
        )
        db.session.add(new_agent)
        db.session.commit()

        return redirect(url_for('agents'))

    # GET request: List all agents belonging to the logged-in user
    agents = Agent.query.filter_by(user_id=user_id).all()
    return render_template('agents.html', agents=agents)

@app.route('/agents/<int:agent_id>/update-prompt', methods=['POST'])
def update_agent_prompt(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    new_prompt = request.form.get('prompt')

    if not new_prompt:
        return redirect(url_for('agents', error="Prompt cannot be empty."))

    agent.prompt = new_prompt
    db.session.commit()

    return redirect(url_for('agents'))

@app.route('/embed', methods=['GET', 'POST'])
@login_required
def embed():
    user_id = session['user_id']
    agents = Agent.query.filter_by(user_id=user_id).all()  # Fetch all agents for the user
    script_tag = None

    if request.method == 'POST':
        try:
            # Fetch form data
            agent_id = request.form.get('agent_id')
            website_url = request.form.get('website_url', '').strip()

            # Validate inputs
            if not agent_id:
                return render_template('embed.html', agents=agents, error="Agent is required.")
            if not website_url:
                return render_template('embed.html', agents=agents, error="Website URL is required.")

            # Get the selected agent
            selected_agent = Agent.query.get_or_404(agent_id)

            # Ensure the agent belongs to the current user
            if selected_agent.user_id != user_id:
                return render_template('embed.html', agents=agents, error="You can only modify your own agents.")

            # Scrape the website data
            scraped_data = scrape_website(website_url)
            if scraped_data.startswith("Error scraping website:"):
                return render_template('embed.html', agents=agents, error=scraped_data)

            # Create or update the chatbot for this agent
            if not selected_agent.chatbot:
                # Create a new chatbot
                new_chatbot = Chatbot(name=f"Chatbot for {selected_agent.name}")
                db.session.add(new_chatbot)
                db.session.commit()
                selected_agent.chatbot_id = new_chatbot.id

            # Update the agent's prompt
            #selected_agent.prompt = scraped_data
            db.session.commit()

            # Generate the embed script
            script_tag = f"<a href='{url_for('chatbot', agent_id=selected_agent.id)}'>Chatbot for {selected_agent.name}</a>"

        except Exception as e:
            db.session.rollback()  # Rollback in case of any database error
            app.logger.error(f"Error in /embed: {e}")  # Log the error for debugging
            return render_template('embed.html', agents=agents, error="An unexpected error occurred. Please try again.")

    return render_template('embed.html', agents=agents, script_tag=script_tag)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    agent_id = request.args.get('agent_id')
    agent = Agent.query.get_or_404(agent_id)
    response = None

    if request.method == 'POST':
        try:
            data = request.get_json()
            user_message = data.get('user_message', '')

            # Generate chatbot response
            response = create_chatbot_response(agent.prompt, user_message)

            # Save the interaction to the database
            new_message = Message(
                message=user_message,
                response=response,
                user_id=agent.user_id,  # Store the owner of the agent
                #agent_id=agent_id
            )
            db.session.add(new_message)
            db.session.commit()

            # Return JSON response
            return {"response": response}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Log the error for debugging
            return {"error": "Failed to process the message"}, 500

    return render_template('chatbot.html', agent=agent)

@app.route('/messages', methods=['GET'])
@login_required
def messages():
    user_id = session['user_id']
    messages = Message.query.filter_by(user_id=user_id).all()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
