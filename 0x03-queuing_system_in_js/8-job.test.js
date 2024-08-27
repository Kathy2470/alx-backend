import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
  const queue = kue.createQueue();
  queue.testMode = true;

  beforeEach(() => {
    queue.testMode.jobs = [];
  });

  afterEach(() => {
    queue.testMode.jobs = [];
  });

  after(() => {
    queue.testMode = false;
    queue.shutdown(0);
  });

  it('display a error message if jobs is not an array', () => {
    const jobs = 'not an array';
    expect(() => createPushNotificationsJobs(jobs, queue)).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.be(2);
    expect(queue.testMode.jobs[0].type).to.be('push_notification_code_3');
    expect(queue.testMode.jobs[1].type).to.be('push_notification_code_3');
  });
});
