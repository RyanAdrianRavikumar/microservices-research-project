package com.dissertation.orderservice;

import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    @GetMapping("/health")
    public String healthCheck() {
        return "Service is running";
    }

    @PostMapping
    public String createOrder(@RequestBody Order order) {
        long randomId = Math.round(Math.random() * 1000);
        order.setId(randomId);
        return "Order received: " + order.getQuantity() + "x " + order.getItem() + " (ID: " + order.getId() + ")";
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