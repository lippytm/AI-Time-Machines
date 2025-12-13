const OpenAI = require('openai');
const fs = require('fs');
require('dotenv').config();

/**
 * Fine-Tuning Manager for OpenAI Models
 * Provides utilities to create, manage, and use fine-tuned models for time-machine-related queries
 */
class FineTuningManager {
  constructor(apiKey = null) {
    const key = apiKey || process.env.OPENAI_API_KEY;
    
    if (!key) {
      throw new Error(
        'OpenAI API key is required. Please set OPENAI_API_KEY in your .env file or pass it to the constructor.'
      );
    }

    this.client = new OpenAI({
      apiKey: key,
    });
  }

  /**
   * Upload a training file for fine-tuning
   * @param {string} filePath - Path to the JSONL training file
   * @returns {Promise<Object>} - The uploaded file object
   */
  async uploadTrainingFile(filePath) {
    try {
      const fileStream = fs.createReadStream(filePath);
      const file = await this.client.files.create({
        file: fileStream,
        purpose: 'fine-tune',
      });
      
      console.log(`✓ File uploaded successfully: ${file.id}`);
      return file;
    } catch (error) {
      throw new Error(`Error uploading training file: ${error.message}`);
    }
  }

  /**
   * Create a fine-tuning job
   * @param {string} fileId - The ID of the uploaded training file
   * @param {Object} options - Fine-tuning options
   * @returns {Promise<Object>} - The fine-tuning job object
   */
  async createFineTuningJob(fileId, options = {}) {
    try {
      const job = await this.client.fineTuning.jobs.create({
        training_file: fileId,
        model: options.model || 'gpt-3.5-turbo',
        hyperparameters: {
          n_epochs: options.epochs || 3,
        },
        suffix: options.suffix || 'time-machine',
      });
      
      console.log(`✓ Fine-tuning job created: ${job.id}`);
      return job;
    } catch (error) {
      throw new Error(`Error creating fine-tuning job: ${error.message}`);
    }
  }

  /**
   * Get the status of a fine-tuning job
   * @param {string} jobId - The ID of the fine-tuning job
   * @returns {Promise<Object>} - The job status
   */
  async getJobStatus(jobId) {
    try {
      const job = await this.client.fineTuning.jobs.retrieve(jobId);
      return job;
    } catch (error) {
      throw new Error(`Error retrieving job status: ${error.message}`);
    }
  }

  /**
   * List all fine-tuning jobs
   * @param {number} limit - Maximum number of jobs to return
   * @returns {Promise<Array>} - List of fine-tuning jobs
   */
  async listJobs(limit = 10) {
    try {
      const jobs = await this.client.fineTuning.jobs.list({ limit });
      return jobs.data;
    } catch (error) {
      throw new Error(`Error listing jobs: ${error.message}`);
    }
  }

  /**
   * Cancel a fine-tuning job
   * @param {string} jobId - The ID of the job to cancel
   * @returns {Promise<Object>} - The cancelled job object
   */
  async cancelJob(jobId) {
    try {
      const job = await this.client.fineTuning.jobs.cancel(jobId);
      console.log(`✓ Job cancelled: ${jobId}`);
      return job;
    } catch (error) {
      throw new Error(`Error cancelling job: ${error.message}`);
    }
  }

  /**
   * Get events/logs for a fine-tuning job
   * @param {string} jobId - The ID of the fine-tuning job
   * @returns {Promise<Array>} - List of events
   */
  async getJobEvents(jobId) {
    try {
      const events = await this.client.fineTuning.jobs.listEvents(jobId);
      return events.data;
    } catch (error) {
      throw new Error(`Error retrieving job events: ${error.message}`);
    }
  }

  /**
   * Delete a fine-tuned model
   * @param {string} modelId - The ID of the model to delete
   * @returns {Promise<Object>} - Deletion confirmation
   */
  async deleteModel(modelId) {
    try {
      const result = await this.client.models.delete(modelId);
      console.log(`✓ Model deleted: ${modelId}`);
      return result;
    } catch (error) {
      throw new Error(`Error deleting model: ${error.message}`);
    }
  }
}

module.exports = FineTuningManager;
