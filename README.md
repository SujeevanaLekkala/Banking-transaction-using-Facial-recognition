                                          **💳 Secure Facial Recognition Payment Gateway**

**🔐 Overview**

In today's digital era, online transactions have become an integral part of our daily lives. However, this convenience comes with the risk of unauthorized access and fraudulent activities. To combat these threats, we propose a robust and secure payment gateway that leverages facial recognition and liveness detection to verify user identity before completing any transaction.

**🎯 Objective**

Our goal is to deliver a seamless, personalized, and highly secure transaction experience by integrating biometric authentication into the payment process.

**🛡️ Key Features**
- Facial Recognition-Based Login : Users must register their facial data and pass a liveness detection test to ensure authenticity.
- Haar Cascade Classifier: For rapid and efficient face detection, we utilize a Haar-cascade-based technique to identify faces from input images.
- Grayscale Conversion: Facial images are converted to grayscale to optimize recognition performance and reduce computational overhead.
- Liveness Detection: Prevents spoofing attempts using static images or videos by verifying real-time user presence.
- Secure Access Control: Only authorized users with verified facial data can proceed to the transaction page. Unauthorized attempts are blocked.

**🔄 Workflow**
- User Registration
- Capture facial image
- Perform liveness detection
- Store encrypted facial data
- Login & Verification
- Capture live facial input
- Convert to grayscale
- Match against stored data
- Grant access if verified
  
**🚀 Technologies Used**
- Python
- OpenCV
- Haar Cascade Classifier
- Flask (for web application)
- SQLite (for user data storage)
  
**📌 Future Enhancements**
- Multi-factor authentication
- Integration with blockchain for transaction logging
- Support for mobile platforms


