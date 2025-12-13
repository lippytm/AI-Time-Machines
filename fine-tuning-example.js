/**
 * Fine-Tuning Example Script
 * 
 * This script demonstrates the complete fine-tuning workflow
 * for creating a specialized time-machine AI model.
 * 
 * NOTE: This script will create a fine-tuning job and incur costs.
 * Use with caution and monitor your OpenAI usage dashboard.
 */

const FineTuningManager = require('./src/fine-tuning');

async function main() {
  try {
    console.log('Fine-Tuning Workflow for Time Machine AI\n');
    console.log('⚠️  WARNING: This will incur OpenAI API costs\n');
    
    const manager = new FineTuningManager();
    
    // Step 1: Upload training data
    console.log('Step 1: Uploading training data...');
    console.log('File: datasets/time-machine-training.jsonl\n');
    
    // Uncomment to actually run:
    // const file = await manager.uploadTrainingFile('datasets/time-machine-training.jsonl');
    // console.log(`✓ File uploaded with ID: ${file.id}\n`);
    
    console.log('(Skipped - uncomment code to run)\n');
    
    // Step 2: Create fine-tuning job
    console.log('Step 2: Creating fine-tuning job...');
    
    // Uncomment to actually run (replace FILE_ID with actual file ID):
    // const job = await manager.createFineTuningJob('FILE_ID', {
    //   model: 'gpt-3.5-turbo',
    //   epochs: 3,
    //   suffix: 'time-machine'
    // });
    // console.log(`✓ Job created with ID: ${job.id}\n`);
    
    console.log('(Skipped - uncomment code to run)\n');
    
    // Step 3: Monitor progress
    console.log('Step 3: Monitoring job progress...');
    
    // Uncomment to actually run (replace JOB_ID with actual job ID):
    // const checkStatus = async (jobId) => {
    //   const status = await manager.getJobStatus(jobId);
    //   console.log(`Status: ${status.status}`);
    //   
    //   if (status.status === 'succeeded') {
    //     console.log(`\n✓ Fine-tuning complete!`);
    //     console.log(`Fine-tuned model ID: ${status.fine_tuned_model}`);
    //     return status.fine_tuned_model;
    //   } else if (status.status === 'failed') {
    //     console.log(`\n✗ Fine-tuning failed`);
    //     throw new Error('Fine-tuning failed');
    //   }
    //   
    //   return null;
    // };
    //
    // await checkStatus('JOB_ID');
    
    console.log('(Skipped - uncomment code to run)\n');
    
    // Step 4: Use the fine-tuned model
    console.log('Step 4: Using the fine-tuned model...');
    
    // Uncomment to actually use (replace MODEL_ID with your fine-tuned model):
    // const { ChatGPT } = require('./src/index');
    // const chatgpt = new ChatGPT();
    // chatgpt.setModel('MODEL_ID');
    // const response = await chatgpt.chat('What should I know about time travel safety?');
    // console.log(`Response: ${response}`);
    
    console.log('(Skipped - uncomment code to run)\n');
    
    console.log('='.repeat(60));
    console.log('Fine-tuning workflow demonstration complete!\n');
    console.log('To actually run fine-tuning:');
    console.log('1. Uncomment the code sections in this file');
    console.log('2. Ensure you have sufficient API credits');
    console.log('3. Monitor costs at https://platform.openai.com/usage');
    console.log('4. See docs/FINE_TUNING.md for detailed guide\n');
    
    // List existing jobs (this is safe to run)
    console.log('Listing your recent fine-tuning jobs:');
    try {
      const jobs = await manager.listJobs(5);
      if (jobs.length === 0) {
        console.log('No fine-tuning jobs found.');
      } else {
        jobs.forEach((job, index) => {
          console.log(`${index + 1}. ${job.id} - Status: ${job.status}`);
          if (job.fine_tuned_model) {
            console.log(`   Model: ${job.fine_tuned_model}`);
          }
        });
      }
    } catch (error) {
      console.log(`Could not list jobs: ${error.message}`);
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

module.exports = { main };
