"use client";

import { useState } from "react";
import { Button } from "./ui/button";
import { Modal } from "./ui/modal";
import { toast } from "sonner";

interface ProductCardProps {
  name: string;
  price: number;
  image_url: string;
  placement?: string;
  description: string;
  color_options?: string[];
  dimensions?: {
    width: number;
    height: number;
    depth?: number;
    unit: string;
  };
}

export function ProductCard({
  name,
  price,
  image_url,
  placement,
  description,
  color_options,
  dimensions,
}: ProductCardProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const handleOrder = () => {
    toast.success(`${name} added to cart!`);
  };

  return (
    <>
      <div className="flex flex-col gap-2 p-4 rounded-xl border bg-card text-card-foreground shadow-sm w-full max-w-sm">
        <div className="aspect-square relative rounded-md overflow-hidden">
          <img
            src={image_url}
            alt={name}
            className="object-cover w-full h-full"
          />
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex justify-between items-center">
            <h3 className="font-medium text-sm">{name}</h3>
            <p className="font-medium">${price.toFixed(2)}</p>
          </div>
          {placement && (
            <p className="text-sm text-muted-foreground italic">
              Placement: {placement}
            </p>
          )}
          <div className="flex items-center justify-between mt-2 gap-2">
            <Button variant="outline" size="sm" onClick={() => setIsModalOpen(true)}>
              View Details
            </Button>
            <Button size="sm" onClick={handleOrder}>
              Order
            </Button>
          </div>
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={name}
      >
        <div className="grid gap-4">
          <div className="aspect-square relative rounded-lg overflow-hidden">
            <img
              src={image_url}
              alt={name}
              className="object-cover w-full h-full"
            />
          </div>
          <div className="flex flex-col gap-2">
            <p className="text-lg font-semibold">${price.toFixed(2)}</p>
            <p className="text-muted-foreground">{description}</p>
            {placement && (
              <p className="text-muted-foreground italic">
                Suggested placement: {placement}
              </p>
            )}
            {color_options && (
              <div>
                <p className="font-medium">Available Colors:</p>
                <ul className="list-disc list-inside">
                  {color_options.map((color) => (
                    <li key={color}>{color}</li>
                  ))}
                </ul>
              </div>
            )}
            {dimensions && (
              <div>
                <p className="font-medium">Dimensions:</p>
                <p>
                  {dimensions.width} × {dimensions.height}
                  {dimensions.depth ? ` × ${dimensions.depth}` : ""}{" "}
                  {dimensions.unit}
                </p>
              </div>
            )}
            <Button onClick={handleOrder} className="mt-2">
              Add to Cart
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
