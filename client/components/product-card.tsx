"use client";

import { useState } from "react";
import { Button } from "./ui/button";
import { Modal } from "./ui/modal";
import { toast } from "sonner";
import { Maximize2 } from "lucide-react";

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
    toast.success(`${name} ordered!`);
  };

  return (
    <>
      <div className="flex flex-row gap-4 p-4 rounded-xl border bg-card text-card-foreground shadow-sm max-w-md">
        <div className="relative rounded-md overflow-hidden w-[200px] h-[200px] shrink-0">
          <img
            src={image_url}
            alt={`${name} image`}
            className="object-cover w-full h-full"
          />
        </div>
        <div className="flex flex-col gap-2 flex-1">
          <div className="flex justify-between items-start">
            <h3 className="font-medium text-lg">{name}</h3>
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0"
              onClick={() => setIsModalOpen(true)}
            >
              <Maximize2 size={16} />
            </Button>
          </div>
          <div className="flex flex-col gap-2 mt-auto">
            <div className="flex justify-between items-center">
              <p className="font-medium">${price.toFixed(2)}</p>
              <Button onClick={handleOrder}>Buy</Button>
            </div>
            {placement && (
              <p className="text-sm text-muted-foreground italic">
                Placement: {placement}
              </p>
            )}
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
              Buy
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}
