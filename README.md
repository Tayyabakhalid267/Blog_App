# Blog App - Django Message Board 🎨

A modern Django message board application with beautiful UI animations, 3D icons, and production-ready deployment configuration.

## ✨ Features

- 🎨 **Animated UI**: Gradient animations, glassmorphism effects, and smooth transitions
- 📝 **Post Management**: Create, edit, and delete blog posts
- 👤 **User Profiles**: Customizable user profiles with avatars
- 💬 **Comments**: Interactive comment system
- 🔍 **Search**: Search posts by title and content
- 📱 **Responsive**: Mobile-friendly design
- 🎭 **3D Icons**: Beautiful Fluency icons from Icons8

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ installed
- Git installed

### Installation (Windows PowerShell)

1. **Clone the repository**
```powershell
git clone https://github.com/Tayyabakhalid267/Blog_App.git
cd Blog_App
```

2. **Create virtual environment and activate it**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Run migrations**
```powershell
python manage.py migrate
```

5. **Create a superuser**
```powershell
python manage.py createsuperuser
```

6. **Run the development server**
```powershell
python manage.py runserver
```

7. **Open your browser**
Navigate to http://127.0.0.1:8000/

## 🎯 Usage

- **Home**: View all blog posts
- **Create Post**: Share your thoughts (login required)
- **Profile**: Manage your profile and view your posts
- **Admin Panel**: Access at /admin/ for site management

## 🧪 Testing

```powershell
python manage.py test
```

## 🌐 Deployment

This app is configured for easy deployment on:
- **Railway.app** (Recommended - no credit card required)
- **Render.com**
- **Heroku**

See `DEPLOYMENT_ALTERNATIVES.md` for detailed deployment guides.

### Production Features
✅ WhiteNoise for static files  
✅ PostgreSQL database support  
✅ Gunicorn WSGI server  
✅ Environment-based configuration  
✅ Security settings for production  

## 🛠️ Tech Stack

- **Backend**: Django 5.2.7
- **Language**: Python 3.13.5
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Static Files**: WhiteNoise
- **Server**: Gunicorn
- **Styling**: Custom CSS with animations
- **Icons**: Icons8 3D Fluency

## 📁 Project Structure

```
Blog_App/
├── mb_project/          # Main project settings
├── posts/               # Blog posts app
├── users/               # User authentication
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── requirements.txt     # Python dependencies
├── Procfile            # Deployment config
├── runtime.txt         # Python version
└── manage.py           # Django management
```

## 🔧 Environment Variables

For production deployment, set:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` in production
- `DATABASE_URL`: PostgreSQL connection string (auto-provided by Railway)

## 📝 License

MIT License - feel free to use this project for learning!

## 👨‍💻 Author

**Tayyaba Khalid**
- GitHub: [@Tayyabakhalid267](https://github.com/Tayyabakhalid267)

## 🙏 Acknowledgments

- Icons by [Icons8](https://icons8.com/)
- Built with Django framework
- Inspired by modern blog designs
