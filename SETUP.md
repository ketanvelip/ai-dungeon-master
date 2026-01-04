# Setup Guide

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

## Quick Start with Docker

1. **Clone/Navigate to the project**
   ```bash
   cd ai-dungeon-master
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development Notes

This project is designed to run with Docker. All services (database, backend, frontend) are containerized and orchestrated via Docker Compose.

For hot-reloading during development:
- Backend changes are automatically detected (volume mounted in docker-compose.yml)
- Frontend requires rebuild: `docker-compose up --build frontend`

## Environment Variables

### Required
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional
- `DATABASE_URL`: PostgreSQL connection string (default: postgresql://dungeon_user:dungeon_pass@localhost:5432/dungeon_master)
- `ENVIRONMENT`: development/production (default: development)

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify database exists: `psql -l`

### OpenAI API Issues
- Verify API key is correct
- Check API key has sufficient credits
- Ensure no rate limiting

### Port Conflicts
- Backend uses port 8000
- Frontend uses port 3000 (dev) or 80 (Docker)
- PostgreSQL uses port 5432
- Change ports in docker-compose.yml if needed

## Stopping the Application

```bash
# Stop Docker containers
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

## Project Structure

```
ai-dungeon-master/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Database models
│   │   ├── database.py          # Database connection
│   │   ├── game_engine.py       # Core game logic
│   │   ├── ai_player.py         # AI player agents
│   │   ├── character_generator.py # Character creation
│   │   ├── dm_assistant.py      # DM suggestions
│   │   └── dice.py              # Dice rolling
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameSetup.js     # Campaign creation
│   │   │   ├── GameInterface.js # Main game view
│   │   │   ├── PartyView.js     # Character sheets
│   │   │   ├── ChatLog.js       # Message history
│   │   │   ├── DMInterface.js   # DM input
│   │   │   └── DiceRoller.js    # Dice rolling UI
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Next Steps

1. Create a campaign and generate your AI party
2. Start narrating your adventure
3. Watch your AI players interact and make decisions
4. Use the dice roller for skill checks and combat
5. Get AI suggestions when you need inspiration

Enjoy being the Dungeon Master! 🎲
