# Gardener Site Data Archive

This repository contains raw data pushed by the Raspberry Pi every 15 minutes.

## Structure

- `data/` - Sensor JSONL files and Claude conversations
- `photos/` - Plant photos
- `workspace/` - Claude's working files
- `logs/` - Execution logs (archived)

## CI/CD

GitHub Actions workflow automatically rebuilds the site when new data is pushed.
See `.github/workflows/deploy.yml` for the build pipeline.

## Related Repositories

- Code: [claude-code-the-gardener](https://github.com/mnbf9rca/claude-code-the-gardener)
- Live site: https://plants.cynexia.com
