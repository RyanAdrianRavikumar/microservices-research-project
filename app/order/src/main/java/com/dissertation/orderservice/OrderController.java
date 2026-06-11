package com.dissertation.orderservice;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final InventoryGrpcClient inventoryGrpcClient;

    public OrderController(InventoryGrpcClient inventoryGrpcClient) {
        this.inventoryGrpcClient = inventoryGrpcClient;
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
        String confirmation = "Order received: " + order.getQuantity() + "x " + order.getItem()
                + " (ID: " + order.getId() + ") — stock confirmed via gRPC";
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