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
      <div className="flex flex-col gap-2 p-4 rounded-xl border bg-card text-card-foreground shadow-sm w-full max-w-lg">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-medium text-sm">{name}</h3>
          <Button
            variant="ghost"
            size="sm"
            className="h-8 w-8 p-0"
            onClick={() => setIsModalOpen(true)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M15 3h6v6" />
              <path d="M10 14 21 3" />
              <path d="M18 13v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h6" />
            </svg>
          </Button>
        </div>
        <div className="aspect-square relative rounded-md overflow-hidden">
          <img
            src={image_url}
            alt={name}
            className="object-cover w-full h-full"
          />
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex justify-between items-center mt-2">
            <p className="font-medium">${price.toFixed(2)}</p>
            <Button size="sm" onClick={handleOrder}>
              Add to Cart
            </Button>
          </div>
          {placement && (
            <p className="text-sm text-muted-foreground italic mt-1">
              Placement: {placement}
            </p>
          )}
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
