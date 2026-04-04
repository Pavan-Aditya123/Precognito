import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import { AssetCard } from "./AssetCard";
import { Asset } from "@/lib/types";

describe("Visual Snapshots", () => {
  it("AssetCard should match snapshot", () => {
    const mockAsset: Asset = {
      id: "motor_1",
      name: "Motor 1",
      status: "GREEN",
      lastUpdated: "2026-04-04T12:00:00Z",
      type: "motor",
      location: "Factory Floor A",
      rms: 0.05,
      rul: 150
    };
    
    const { asFragment } = render(<AssetCard asset={mockAsset} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
