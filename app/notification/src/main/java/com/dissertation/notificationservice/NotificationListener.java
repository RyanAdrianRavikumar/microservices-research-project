package com.dissertation.notificationservice;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class NotificationListener {

    @RabbitListener(queues = "notification-queue")
    public void receiveOrder(String message) {
        System.out.println("Notification sent for order: " + message);
        System.out.println("Timestamp: " + LocalDateTime.now());
        System.out.println("----------------------------------------");
    }
}