# CloudWatch Alarm Slack Notifier

This lambda function notifies [CloudWatch Alarm](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
via [Slack Incoming Webhooks](https://api.slack.com/incoming-webhooks).

## HOW TO USE

1. [Create new Amazon CloudWatch Alarms](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
2. [Set Up Amazon SNS Notifications](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/US_SetupSNS.html)
3. Create a new [AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/welcome.html) function by using `lambda_function.py` as the code
4. Add a new trigger which subscribes the Amazon SNS Notification
