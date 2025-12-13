# Fine-Tuning Guide for AI Time Machines

This guide explains how to fine-tune OpenAI models for time-machine-related queries to create more specialized and accurate AI responses.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Training Data Format](#training-data-format)
- [Fine-Tuning Process](#fine-tuning-process)
- [Using Fine-Tuned Models](#using-fine-tuned-models)
- [Best Practices](#best-practices)
- [Cost Considerations](#cost-considerations)

## Overview

Fine-tuning allows you to customize OpenAI's models with your own training data, creating specialized models that better understand time-machine-related queries, historical contexts, and temporal mechanics.

### Benefits of Fine-Tuning

- **Improved accuracy** for time-travel-specific queries
- **Consistent personality** across responses
- **Domain expertise** in historical periods and temporal physics
- **Reduced need for lengthy prompts** (context is built into the model)
- **Better performance** on specialized tasks

## Prerequisites

Before you begin fine-tuning, ensure you have:

1. **OpenAI API Key** with fine-tuning access
2. **Training data** in JSONL format (see [Training Data Format](#training-data-format))
3. **Node.js** 18.0.0 or higher
4. **Sufficient API credits** (fine-tuning incurs costs)

## Training Data Format

Fine-tuning data must be in JSONL format (JSON Lines), where each line is a JSON object representing a conversation.

### Format Structure

```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

### Example Training Data

```jsonl
{"messages": [{"role": "system", "content": "You are a Time Machine AI assistant."}, {"role": "user", "content": "How does a time machine work?"}, {"role": "assistant", "content": "Time machines operate on spacetime manipulation principles..."}]}
{"messages": [{"role": "system", "content": "You are a Time Machine AI assistant."}, {"role": "user", "content": "What would I see in ancient Rome?"}, {"role": "assistant", "content": "In ancient Rome around 100 CE, you would see..."}]}
```

### Data Quality Guidelines

- **Minimum examples**: 10 examples (50-100 recommended for good results)
- **Consistency**: Use the same system message across examples
- **Diversity**: Cover various aspects of time travel (history, physics, safety, paradoxes)
- **Quality over quantity**: Well-crafted examples are better than many poor ones
- **Accuracy**: Ensure historical and scientific accuracy in responses

### Included Dataset

This repository includes a sample training dataset at `datasets/time-machine-training.jsonl` with examples covering:

- Time travel mechanics
- Historical periods and events
- Temporal paradoxes
- Safety considerations
- Cultural context for different eras

## Fine-Tuning Process

### Step 1: Prepare Your Training Data

Create or modify a JSONL file with your training examples:

```bash
# Use the included dataset
cp datasets/time-machine-training.jsonl datasets/my-training-data.jsonl

# Or create your own
nano datasets/my-training-data.jsonl
```

### Step 2: Upload Training File

```javascript
const FineTuningManager = require('./src/fine-tuning');

async function uploadData() {
  const manager = new FineTuningManager();
  
  // Upload training file
  const file = await manager.uploadTrainingFile('datasets/time-machine-training.jsonl');
  console.log('File ID:', file.id);
  
  return file.id;
}
```

### Step 3: Create Fine-Tuning Job

```javascript
async function startFineTuning(fileId) {
  const manager = new FineTuningManager();
  
  const job = await manager.createFineTuningJob(fileId, {
    model: 'gpt-3.5-turbo',  // Base model to fine-tune
    epochs: 3,                // Number of training epochs
    suffix: 'time-machine'    // Suffix for model name
  });
  
  console.log('Job ID:', job.id);
  return job.id;
}
```

### Step 4: Monitor Progress

```javascript
async function monitorJob(jobId) {
  const manager = new FineTuningManager();
  
  // Check status
  const status = await manager.getJobStatus(jobId);
  console.log('Status:', status.status);
  console.log('Fine-tuned model:', status.fine_tuned_model);
  
  // Get training events
  const events = await manager.getJobEvents(jobId);
  events.forEach(event => {
    console.log(`[${event.created_at}] ${event.message}`);
  });
}
```

### Step 5: Complete Example Script

```javascript
const FineTuningManager = require('./src/fine-tuning');

async function completeFinetuneWorkflow() {
  const manager = new FineTuningManager();
  
  // Step 1: Upload training data
  console.log('Uploading training data...');
  const file = await manager.uploadTrainingFile('datasets/time-machine-training.jsonl');
  console.log(`✓ File uploaded: ${file.id}`);
  
  // Step 2: Create fine-tuning job
  console.log('\nCreating fine-tuning job...');
  const job = await manager.createFineTuningJob(file.id, {
    model: 'gpt-3.5-turbo',
    epochs: 3,
    suffix: 'time-machine'
  });
  console.log(`✓ Job created: ${job.id}`);
  
  // Step 3: Monitor until complete
  console.log('\nMonitoring job progress...');
  let jobStatus;
  do {
    await new Promise(resolve => setTimeout(resolve, 60000)); // Wait 1 minute
    jobStatus = await manager.getJobStatus(job.id);
    console.log(`Status: ${jobStatus.status}`);
  } while (jobStatus.status === 'running' || jobStatus.status === 'queued');
  
  if (jobStatus.status === 'succeeded') {
    console.log(`\n✓ Fine-tuning complete!`);
    console.log(`Model ID: ${jobStatus.fine_tuned_model}`);
    return jobStatus.fine_tuned_model;
  } else {
    console.error(`\n✗ Fine-tuning failed: ${jobStatus.status}`);
    throw new Error('Fine-tuning failed');
  }
}
```

## Using Fine-Tuned Models

Once your model is fine-tuned, use it with the ChatGPT class:

```javascript
const { ChatGPT } = require('./src/index');

async function useFineTunedModel() {
  const chatgpt = new ChatGPT();
  
  // Set your fine-tuned model
  chatgpt.setModel('ft:gpt-3.5-turbo:your-org:time-machine:abc123');
  
  // Use as normal
  const response = await chatgpt.chat('What should I know before visiting ancient Egypt?');
  console.log(response);
}
```

### Integration with Agents

```javascript
const TimeTravelAssistant = require('./agents/time-travel-assistant');

async function useFineTunedAgent() {
  const assistant = new TimeTravelAssistant();
  
  // The agent uses ChatGPT internally, so set the model
  assistant.chatgpt.setModel('ft:gpt-3.5-turbo:your-org:time-machine:abc123');
  
  const response = await assistant.chat('Plan a trip to the Renaissance');
  console.log(response);
}
```

## Best Practices

### Training Data

1. **Quality First**: Focus on high-quality, accurate examples
2. **Consistent Voice**: Maintain consistent personality and tone
3. **Diverse Topics**: Cover all aspects of your use case
4. **Validate Data**: Check for errors, inconsistencies, and biases
5. **Incremental Updates**: Start small, test, then expand

### Model Selection

- **gpt-3.5-turbo**: Cost-effective, good for most use cases
- **gpt-4**: Higher quality but more expensive to fine-tune
- Start with gpt-3.5-turbo and upgrade if needed

### Training Parameters

- **Epochs**: Start with 3-4, adjust based on results
  - Too few: Underfit (poor performance)
  - Too many: Overfit (memorization, poor generalization)
- **Learning Rate**: Usually auto-configured by OpenAI

### Testing and Validation

1. **Reserve test data**: Hold back 10-20% of examples for testing
2. **Compare models**: Test fine-tuned vs. base model
3. **Real-world testing**: Test with actual user queries
4. **Iterate**: Refine based on results

### Cost Management

- **Start small**: Test with 10-50 examples first
- **Monitor costs**: Track fine-tuning and inference costs
- **Cache responses**: Reduce repeated API calls
- **Use appropriate models**: Don't over-spec for simple tasks

## Cost Considerations

### Fine-Tuning Costs

Fine-tuning costs depend on:
- Number of tokens in training data
- Number of epochs
- Base model used

**Estimated costs** (as of 2024):
- Training: ~$0.008 per 1K tokens for gpt-3.5-turbo
- Usage: ~$0.012 per 1K tokens (input) for fine-tuned gpt-3.5-turbo

### Example Cost Calculation

For 100 training examples averaging 300 tokens each:
- Total tokens: 100 × 300 = 30,000 tokens
- 3 epochs: 30,000 × 3 = 90,000 tokens
- Cost: 90,000 / 1,000 × $0.008 = **~$0.72**

Usage costs are typically higher than base models but provide better results.

### Cost Optimization

- Start with smaller datasets
- Use gpt-3.5-turbo instead of gpt-4
- Optimize prompt length in training data
- Monitor and analyze usage patterns

## Management Commands

### List All Fine-Tuning Jobs

```javascript
const manager = new FineTuningManager();
const jobs = await manager.listJobs(10);
jobs.forEach(job => {
  console.log(`${job.id}: ${job.status} - ${job.fine_tuned_model || 'pending'}`);
});
```

### Cancel a Running Job

```javascript
const manager = new FineTuningManager();
await manager.cancelJob('ftjob-abc123');
```

### Delete a Fine-Tuned Model

```javascript
const manager = new FineTuningManager();
await manager.deleteModel('ft:gpt-3.5-turbo:your-org:time-machine:abc123');
```

## Troubleshooting

### Common Issues

**Error: "Training file format is invalid"**
- Ensure JSONL format (one JSON object per line)
- Validate JSON syntax
- Check that messages array follows the correct structure

**Error: "Insufficient training examples"**
- Provide at least 10 examples
- OpenAI recommends 50-100 for best results

**Poor model performance**
- Increase training examples
- Improve data quality
- Adjust number of epochs
- Ensure diverse and representative examples

**High costs**
- Reduce token count in examples
- Use fewer epochs
- Start with smaller dataset

## Resources

- [OpenAI Fine-Tuning Documentation](https://platform.openai.com/docs/guides/fine-tuning)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/fine-tuning)
- [Best Practices Guide](https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset)
- [Pricing Information](https://openai.com/pricing)

## Support

For questions and issues:
- [GitHub Issues](https://github.com/lippytm/AI-Time-Machines/issues)
- [GitHub Discussions](https://github.com/lippytm/AI-Time-Machines/discussions)
- [OpenAI Community Forum](https://community.openai.com/)

---

Happy fine-tuning! 🚀⏰
