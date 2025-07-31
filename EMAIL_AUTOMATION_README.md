# Real InvestCo Email Automation System

## Overview

The Real InvestCo website now includes a comprehensive email automation system built with Firebase Functions and Brevo (formerly Sendinblue). This system handles contact form submissions, drip campaigns, scheduled emails, and provides detailed analytics.

## Features

### 🚀 Core Email Automation
- **Automatic Contact Form Responses** - Immediate confirmation emails when someone submits a contact form
- **Drip Campaigns** - Multi-email sequences with configurable delays
- **Scheduled Emails** - Send emails at specific dates and times
- **Bulk Email Operations** - Send emails to multiple contacts at once
- **Email Templates** - Reusable HTML email templates with variables

### 📊 Analytics & Management
- **Email Analytics Dashboard** - Track open rates, delivery rates, and engagement
- **Campaign Management** - Create, edit, and monitor drip campaigns
- **Contact Management** - Add contacts to campaigns and manage subscriptions
- **Template Management** - Create and edit email templates

### 🔧 Technical Features
- **Firebase Integration** - Secure data storage and real-time updates
- **Brevo API Integration** - Professional email delivery service
- **Webhook System** - Flexible email sending via HTTP requests
- **Unsubscribe Management** - GDPR-compliant unsubscribe functionality

## System Architecture

### Firebase Collections
- `generalInquiries` - General contact form submissions
- `propertyInquiries` - Property-specific contact form submissions
- `emailLogs` - All email sending activity and results
- `scheduledEmails` - Emails scheduled for future delivery
- `dripCampaigns` - Drip campaign configurations
- `campaignSubscriptions` - Contact subscriptions to campaigns
- `emailTemplates` - Reusable email templates
- `unsubscribedEmails` - Users who have unsubscribed

### Firebase Functions
- `sendEmailWebhook` - Main email sending function
- `scheduleEmail` - Schedule emails for future delivery
- `processScheduledEmails` - Automated processing of scheduled emails
- `createDripCampaign` - Create new drip campaigns
- `addToDripCampaign` - Add contacts to campaigns
- `processDripCampaigns` - Automated drip campaign processing
- `getEmailAnalytics` - Retrieve email performance data
- `saveEmailTemplate` - Save/update email templates
- `getEmailTemplates` - Retrieve email templates
- `deleteEmailTemplate` - Delete email templates
- `sendBulkEmail` - Send emails to multiple contacts
- `unsubscribeFromEmails` - Handle unsubscribe requests

## Email Templates

### Built-in Templates
1. **inbound_confirmation** - Auto-sent when someone submits a contact form
2. **outbound_welcome** - Welcome email for new contacts
3. **outbound_followup** - Follow-up email for existing contacts
4. **custom** - Custom template with dynamic content

### Template Variables
- `{{name}}` - Contact's name
- `{{email}}` - Contact's email
- `{{cellPhone}}` - Contact's cell phone
- `{{landline}}` - Contact's landline
- `{{message}}` - Original message from contact form
- `{{propertyTitle}}` - Property title (for property inquiries)

## Admin Panel Access

### Email Automation Dashboard
Access the email automation dashboard at: `/admin-email-automation.html`

**Features:**
- Overview dashboard with key metrics
- Drip campaign creation and management
- Scheduled email management
- Email analytics and reporting
- Template management

### Navigation
From the main admin panel (`/admin-secret.html`), click the "Email Automation" button to access the email automation dashboard.

## Setup Instructions

### 1. Firebase Configuration
Ensure your Firebase project has the following services enabled:
- Firestore Database
- Cloud Functions
- Authentication

### 2. Brevo API Key
Set your Brevo API key in Firebase Functions config:
```bash
firebase functions:config:set brevo.key="your-brevo-api-key"
```

### 3. Deploy Functions
Deploy the Firebase Functions:
```bash
firebase deploy --only functions
```

### 4. Email Templates
The system comes with pre-built email templates. You can customize them by editing the `functions/index.js` file in the `sendEmailWebhook` function.

## Usage Examples

### Creating a Drip Campaign
1. Go to Email Automation Dashboard
2. Click "Create New Campaign"
3. Set campaign name and description
4. Add email sequence with delays
5. Save campaign

### Scheduling an Email
1. Go to "Scheduled Emails" tab
2. Click "Schedule New Email"
3. Select contact and template
4. Set date and time
5. Schedule email

### Sending Bulk Emails
1. Select contacts from submissions
2. Choose email template
3. Send to all selected contacts

## Email Flow Examples

### New Contact Form Submission
1. User submits contact form
2. Data saved to Firestore (`generalInquiries` or `propertyInquiries`)
3. Automatic confirmation email sent (`inbound_confirmation`)
4. Admin notification email sent
5. Contact added to Brevo (if newsletter checked)

### Drip Campaign Flow
1. Contact added to drip campaign
2. First email scheduled (with delay if specified)
3. Email sent automatically
4. Next email scheduled based on campaign sequence
5. Process continues until campaign completion

## Best Practices

### Email Content
- Keep subject lines clear and compelling
- Use personalization variables
- Include clear call-to-action buttons
- Provide unsubscribe links
- Test emails before sending

### Campaign Management
- Start with simple campaigns
- Monitor analytics regularly
- A/B test different templates
- Respect unsubscribe requests
- Follow email marketing best practices

### Technical Considerations
- Monitor Firebase Functions logs
- Set up error alerts
- Regular backup of email templates
- Test webhook endpoints
- Monitor Brevo API usage

## Troubleshooting

### Common Issues

**Emails not sending:**
- Check Brevo API key configuration
- Verify Firebase Functions are deployed
- Check function logs for errors

**Scheduled emails not processing:**
- Ensure `processScheduledEmails` function is deployed
- Check Firestore rules allow function access
- Verify scheduled time format

**Campaign emails not progressing:**
- Check `processDripCampaigns` function
- Verify campaign configuration
- Check contact subscription status

### Debugging
1. Check Firebase Functions logs
2. Verify Firestore data structure
3. Test webhook endpoints manually
4. Check Brevo dashboard for delivery status

## Security Considerations

- All API keys stored in Firebase config
- CORS properly configured for webhooks
- Input validation on all functions
- Rate limiting on email sending
- Unsubscribe functionality for GDPR compliance

## Support

For technical support or questions about the email automation system:
1. Check Firebase Functions logs
2. Review this documentation
3. Test individual components
4. Contact development team

## Future Enhancements

Potential improvements for the email automation system:
- Email open/click tracking
- Advanced segmentation
- A/B testing capabilities
- Integration with CRM systems
- Advanced analytics dashboard
- Mobile app notifications
- SMS integration
- Social media integration 