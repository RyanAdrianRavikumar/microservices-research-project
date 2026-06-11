package com.dissertation.inventoryservice;

import com.dissertation.inventoryservice.grpc.InventoryProto;
import com.dissertation.inventoryservice.grpc.InventoryServiceGrpc;
import io.grpc.stub.StreamObserver;
import org.springframework.stereotype.Service;

@Service
public class InventoryServiceImpl extends InventoryServiceGrpc.InventoryServiceImplBase {

    @Override
    public void checkStock(InventoryProto.CheckStockRequest request,
                           StreamObserver<InventoryProto.StockResponse> responseObserver) {

        System.out.println("gRPC call received for item: " + request.getItemName());

        InventoryProto.StockResponse response = InventoryProto.StockResponse.newBuilder()
                .setInStock(true)
                .setMessage("Item available: " + request.getItemName())
                .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}