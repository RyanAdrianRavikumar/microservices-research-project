package com.dissertation.orderservice;

import com.dissertation.inventoryservice.grpc.InventoryProto;
import com.dissertation.inventoryservice.grpc.InventoryServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class InventoryGrpcClient {

    private static final Logger log = LoggerFactory.getLogger(InventoryGrpcClient.class);

    private ManagedChannel channel;
    private InventoryServiceGrpc.InventoryServiceBlockingStub blockingStub;

    @PostConstruct
    public void init() {
        this.channel = ManagedChannelBuilder
                .forAddress("localhost", 9090)
                .usePlaintext()
                .build();
        this.blockingStub = InventoryServiceGrpc.newBlockingStub(channel);
    }

    public boolean checkStock(String itemName) {
        InventoryProto.CheckStockRequest request = InventoryProto.CheckStockRequest
                .newBuilder()
                .setItemName(itemName)
                .build();

        InventoryProto.StockResponse response = blockingStub.checkStock(request);

        log.info("gRPC response from inventory-service: {}", response.getMessage());
        return response.getInStock();
    }

    @PreDestroy
    public void shutdown() {
        if (channel != null && !channel.isShutdown()) {
            channel.shutdown();
        }
    }
}