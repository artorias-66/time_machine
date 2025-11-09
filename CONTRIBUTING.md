# Contributing to Time Machine for Earth

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/time-machine-earth/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, browser, Node/Python versions)

### Suggesting Features

1. Check existing [Issues](https://github.com/yourusername/time-machine-earth/issues) for similar suggestions
2. Create a new issue with tag `enhancement`
3. Describe:
   - The problem it solves
   - Proposed solution
   - Alternative solutions considered
   - Additional context

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Add tests if applicable

4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
   
   Use conventional commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `style:` Formatting
   - `refactor:` Code restructuring
   - `test:` Tests
   - `chore:` Maintenance

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Describe what changed and why
   - Reference related issues
   - Include screenshots for UI changes

## Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Local Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/time-machine-earth.git
cd time-machine-earth

# Install dependencies
cd frontend && npm install && cd ..
cd backend && pip install -r requirements.txt && cd ..

# Run in development mode
# Terminal 1:
cd backend && python -m uvicorn main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

## Code Style

### Frontend (JavaScript/React)
- Use ESLint configuration (`.eslintrc.cjs`)
- 2 spaces for indentation
- Functional components with hooks
- Descriptive variable names
- Comments for complex logic

```javascript
// Good
const handleSubmit = async (formData) => {
  // Validate before submission
  if (!validateForm(formData)) return
  
  await submitData(formData)
}

// Bad
const h = async (d) => {
  if (!v(d)) return
  await s(d)
}
```

### Backend (Python)
- Follow PEP 8
- 4 spaces for indentation
- Type hints where applicable
- Docstrings for functions and classes

```python
# Good
async def fetch_images(
    bounds: Dict[str, float],
    start_date: str,
    end_date: str
) -> List[Dict]:
    """
    Fetch satellite images for the specified parameters.
    
    Args:
        bounds: Geographic boundaries
        start_date: ISO format date string
        end_date: ISO format date string
        
    Returns:
        List of image dictionaries
    """
    pass

# Bad
async def fetch(b,s,e):
    pass
```

## Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
pytest
```

### Manual Testing Checklist
- [ ] Draw AOI on map
- [ ] Select date range
- [ ] Adjust parameters
- [ ] Generate timelapse (GIF)
- [ ] Generate timelapse (MP4)
- [ ] Download result
- [ ] Test dark mode
- [ ] Test on mobile
- [ ] Check error handling

## Project Structure

```
time-machine-earth/
├── frontend/           # React application
│   ├── src/
│   │   ├── components/ # React components
│   │   └── App.jsx     # Main app
│   └── package.json
├── backend/            # FastAPI application
│   ├── services/       # Business logic
│   ├── main.py         # API endpoints
│   └── requirements.txt
└── docs/              # Additional documentation
```

## Areas for Contribution

### High Priority
- [ ] Real satellite API integration (Arlula, USGS, Sentinel)
- [ ] Unit and integration tests
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Accessibility improvements

### Medium Priority
- [ ] Additional visualization types
- [ ] User authentication
- [ ] Save/load projects
- [ ] Batch processing
- [ ] Mobile app

### Good First Issues
- [ ] Documentation improvements
- [ ] UI/UX enhancements
- [ ] Bug fixes
- [ ] Adding example configurations
- [ ] Improving error messages

## Satellite API Integration

Want to add real satellite data? Here's how:

### 1. Choose an API
- Arlula Archive API
- USGS Landsat
- Sentinel Hub
- AgroMonitoring

### 2. Implementation Steps
1. Add API credentials to `.env`
2. Implement in `backend/services/satellite_service.py`
3. Add tests
4. Update documentation
5. Submit PR

### Example Template

```python
async def fetch_from_new_api(
    self,
    bounds: Dict,
    start_date: str,
    end_date: str
) -> List[Dict]:
    """Fetch from New Satellite API."""
    # Your implementation here
    pass
```

## Documentation

### When to Update Docs
- New features → Update README.md
- API changes → Update ARCHITECTURE.md
- Deployment changes → Update DEPLOYMENT.md
- New dependencies → Update requirements.txt or package.json

### Documentation Style
- Clear and concise
- Include code examples
- Add diagrams where helpful
- Keep up to date

## Community Guidelines

### Be Respectful
- Treat everyone with respect
- Assume good intentions
- Provide constructive feedback
- Welcome newcomers

### Communication
- Use clear, professional language
- Stay on topic
- Be patient with responses
- Help others when you can

## Questions?

- Open an issue with the `question` label
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Time Machine for Earth! 🌍✨**


