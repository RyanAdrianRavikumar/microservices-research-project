package com.dissertation.orderservice;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private static final Logger logger = LoggerFactory.getLogger(OrderController.class);

    private final InventoryGrpcClient inventoryGrpcClient;
    private final RabbitTemplate rabbitTemplate;

    public OrderController(InventoryGrpcClient inventoryGrpcClient, RabbitTemplate rabbitTemplate) {
        this.inventoryGrpcClient = inventoryGrpcClient;
        this.rabbitTemplate = rabbitTemplate;
    }

    @GetMapping("/health")
    public String healthCheck() {
        return "Service is running";
    }

    @PostMapping
    public ResponseEntity<String> createOrder(@RequestBody Order order) {
        boolean inStock = inventoryGrpcClient.checkStock(order.getItem());

        if (!inStock) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body("Order rejected: item not in stock");
        }

        long randomId = Math.round(Math.random() * 1000);
        order.setId(randomId);

        String messageString = "Order{id=" + order.getId() + ", item=" + order.getItem() +
                ", quantity=" + order.getQuantity() + "}";
        rabbitTemplate.convertAndSend("orders-exchange", "order.created", messageString);
        logger.info("Published to RabbitMQ: " + messageString);

        String confirmation = "Order received: " + order.getQuantity() + "x " + order.getItem()
                + " (ID: " + order.getId() + ") — stock confirmed, notification queued";
        return ResponseEntity.ok(confirmation);
    }

    @GetMapping
    public List<Order> getAllOrders() {
        List<Order> orders = new ArrayList<>();
        orders.add(new Order(1L, "Book", 2));
        orders.add(new Order(2L, "Pen", 5));
        orders.add(new Order(3L, "Laptop", 1));
        return orders;
    }
}