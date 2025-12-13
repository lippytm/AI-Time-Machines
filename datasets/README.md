# Training Datasets

This directory contains training datasets for fine-tuning OpenAI models to specialize in time-machine-related queries.

## Available Datasets

### time-machine-training.jsonl

A curated dataset of time-travel-related conversations covering:

- **Time travel mechanics**: How time machines work, theoretical physics
- **Historical periods**: Information about various time periods and events
- **Temporal paradoxes**: Grandfather paradox, bootstrap paradox, causality
- **Safety considerations**: Risks and precautions for time travel
- **Cultural context**: What to expect in different historical eras

**Format**: JSONL (JSON Lines)  
**Examples**: 10 conversation samples  
**Purpose**: Fine-tuning base models for time-machine domain expertise

## Using Training Data

### Basic Usage

```javascript
const { FineTuningManager } = require('../src/index');

const manager = new FineTuningManager();

// Upload the training file
const file = await manager.uploadTrainingFile('datasets/time-machine-training.jsonl');

// Create fine-tuning job
const job = await manager.createFineTuningJob(file.id);
```

### File Format

Each line in the JSONL file is a complete conversation:

```jsonl
{"messages": [{"role": "system", "content": "System prompt"}, {"role": "user", "content": "User question"}, {"role": "assistant", "content": "AI response"}]}
```

## Creating Your Own Dataset

### Guidelines

1. **Consistency**: Use the same system message across all examples
2. **Quality**: Focus on accurate, well-written examples
3. **Diversity**: Cover different aspects of your domain
4. **Format**: Follow OpenAI's JSONL format exactly

### Example Template

```jsonl
{"messages": [{"role": "system", "content": "You are a Time Machine AI assistant that helps users understand and explore different time periods."}, {"role": "user", "content": "Your question here"}, {"role": "assistant", "content": "The ideal response"}]}
```

### Validation

Before uploading, validate your JSONL file:

```bash
# Check JSON syntax
cat your-dataset.jsonl | while read line; do echo $line | jq .; done

# Count examples
wc -l your-dataset.jsonl
```

## Best Practices

- **Start small**: 10-50 examples for initial testing
- **Iterate**: Test, evaluate, and expand your dataset
- **Accuracy**: Ensure factual accuracy in all responses
- **Variety**: Include different question types and scenarios
- **Balance**: Cover all important aspects of your domain

## Resources

- [OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [Dataset Preparation](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)
- [Fine-Tuning Documentation](../docs/FINE_TUNING.md)

## Adding New Datasets

To contribute a new dataset:

1. Create a JSONL file following the format above
2. Add documentation in this README
3. Test with a small fine-tuning job
4. Submit a pull request

## Support

For questions about datasets or fine-tuning:
- See [docs/FINE_TUNING.md](../docs/FINE_TUNING.md)
- Open an issue on GitHub
- Visit [OpenAI Community Forum](https://community.openai.com/)
