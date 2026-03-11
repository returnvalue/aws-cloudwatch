# AWS CloudWatch Monitoring Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-CloudWatch_Monitoring-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon CloudWatch concepts, from log management and metric filtering to automated alarms and dashboards. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS monitoring environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Log Management:** Creating log groups and streams to centralize application logs.
* **Metric Filters:** Automatically extracting numerical data from text logs for monitoring.
* **CloudWatch Alarms:** (Upcoming) Setting thresholds to trigger notifications or automated actions.
* **Custom Metrics:** (Upcoming) Publishing application-specific data points.
* **Dashboards:** (Upcoming) Visualizing infrastructure health and performance.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving monitoring infrastructure.

## 📚 Labs Index
1. [Lab 1: CloudWatch Logs & Metric Filters](./labs/lab1-cloudwatch-logs/README.md)
