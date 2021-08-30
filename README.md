#Welcome
My name is Xavier Castillo-Vieira and I started this project in the Summer of 2021 while working as a research assistance under Professor Hiaying Shen at the University of Virginia. My research topic was employing machine models using cloud computing. A couple weeks into my research, I decided to learn the AWS Cloud Development Toolkit to better understand how cloud computing works.

This project is my first solo cloud computing endeavor. It is the basic backend of a banking system, employing different AWS services, such as lambda functions, dynamoDB tables and s3 buckets. I decided to also add a simple HTTP API abstraction layer. 

In the future, I'd like to fine-tune the HTTP API on this project as well as shave off unecessary permissions assigned to lambda functions. For example, if a Lambda only uses dynamodb.get_item(), I would grant it only that command and not all of the read permissions.
