/**
 * Fine-Tuning Example Script
 * 
 * This script demonstrates the complete fine-tuning workflow
 * for creating a specialized time-machine AI model.
 * 
 * By default, this runs in DEMO MODE which shows the workflow
 * without making actual API calls. Set DEMO_MODE to false to
 * actually run fine-tuning (which incurs costs).
 */

const FineTuningManager = require('./src/fine-tuning');

// DEMO MODE: Set to false to actually run fine-tuning
const DEMO_MODE = true;

async function demoWorkflow() {
  console.log('Fine-Tuning Workflow Demonstration\n');
  console.log('Running in DEMO MODE - no actual API calls will be made\n');
  
  console.log('Step 1: Upload training data');
  console.log('  File: datasets/time-machine-training.jsonl');
  console.log('  → This uploads your JSONL training file to OpenAI');
  console.log('  → Returns a file ID to use in the next step\n');
  
  console.log('Step 2: Create fine-tuning job');
  console.log('  Parameters:');
  console.log('    - model: gpt-3.5-turbo (base model)');
  console.log('    - epochs: 3 (training iterations)');
  console.log('    - suffix: time-machine (for model naming)');
  console.log('  → Creates a fine-tuning job');
  console.log('  → Returns a job ID to monitor progress\n');
  
  console.log('Step 3: Monitor job progress');
  console.log('  → Poll job status until complete');
  console.log('  → View training events and metrics');
  console.log('  → Typical completion time: 10-30 minutes\n');
  
  console.log('Step 4: Use the fine-tuned model');
  console.log('  → Once complete, get the fine-tuned model ID');
  console.log('  → Use it with ChatGPT or agents');
  console.log('  → Model will have specialized knowledge\n');
  
  console.log('='.repeat(60));
  console.log('\nTo run actual fine-tuning:');
  console.log('1. Set DEMO_MODE = false in this file');
  console.log('2. Ensure you have sufficient API credits');
  console.log('3. Monitor costs at https://platform.openai.com/usage');
  console.log('4. See docs/FINE_TUNING.md for detailed guide\n');
}

async function actualWorkflow() {
  console.log('Fine-Tuning Workflow for Time Machine AI\n');
  console.log('⚠️  WARNING: This will incur OpenAI API costs\n');
  
  const manager = new FineTuningManager();
  
  try {
    // Step 1: Upload training data
    console.log('Step 1: Uploading training data...');
    console.log('File: datasets/time-machine-training.jsonl\n');
    
    const file = await manager.uploadTrainingFile('datasets/time-machine-training.jsonl');
    console.log(`✓ File uploaded with ID: ${file.id}\n`);
    
    // Step 2: Create fine-tuning job
    console.log('Step 2: Creating fine-tuning job...');
    
    const job = await manager.createFineTuningJob(file.id, {
      model: 'gpt-3.5-turbo',
      epochs: 3,
      suffix: 'time-machine'
    });
    console.log(`✓ Job created with ID: ${job.id}\n`);
    
    // Step 3: Monitor progress (initial check only)
    console.log('Step 3: Checking initial job status...');
    const status = await manager.getJobStatus(job.id);
    console.log(`Status: ${status.status}\n`);
    
    console.log('Fine-tuning job has been started!');
    console.log('\nTo monitor progress, run:');
    console.log(`  const status = await manager.getJobStatus('${job.id}');`);
    console.log('\nTo check events:');
    console.log(`  const events = await manager.getJobEvents('${job.id}');`);
    console.log('\nThe job typically takes 10-30 minutes to complete.\n');
    
    return job.id;
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    throw error;
  }
}

async function main() {
  try {
    if (DEMO_MODE) {
      await demoWorkflow();
    } else {
      await actualWorkflow();
    }
    
    // List existing jobs (safe to run in both modes)
    console.log('\nListing your recent fine-tuning jobs:');
    try {
      const manager = new FineTuningManager();
      const jobs = await manager.listJobs(5);
      
      if (jobs.length === 0) {
        console.log('No fine-tuning jobs found.');
      } else {
        console.log();
        jobs.forEach((job, index) => {
          console.log(`${index + 1}. ${job.id}`);
          console.log(`   Status: ${job.status}`);
          if (job.fine_tuned_model) {
            console.log(`   Model: ${job.fine_tuned_model}`);
          }
          console.log();
        });
      }
    } catch (error) {
      if (DEMO_MODE) {
        console.log('(API call skipped in demo mode)');
      } else {
        console.log(`Could not list jobs: ${error.message}`);
      }
    }
    
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    console.error('\nMake sure you have:');
    console.error('1. Created a .env file with your OPENAI_API_KEY');
    console.error('2. Sufficient API credits in your OpenAI account');
    console.error('3. Fine-tuning access (may require paid tier)');
    process.exit(1);
  }
}

// Run the example
if (require.main === module) {
  main();
}

module.exports = { main, DEMO_MODE };
