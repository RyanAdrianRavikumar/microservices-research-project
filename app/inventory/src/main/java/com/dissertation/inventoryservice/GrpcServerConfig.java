package com.dissertation.inventoryservice;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;

@Configuration
public class GrpcServerConfig {

    @Bean
    public Server grpcServer(InventoryServiceImpl inventoryService) throws IOException {
        Server server = ServerBuilder.forPort(9090)
                .addService(inventoryService)
                .build();

        server.start();

        System.out.println("gRPC server started on port 9090");

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutting down gRPC server...");
            server.shutdown();
        }));

        return server;
    }
}