import { dashboardSample } from "@/sampleAgentData/dashboard";
import { deleteSurfaceSample } from "@/sampleAgentData/deleteSurface";
import { formSample } from "@/sampleAgentData/form";
import { gallerySample } from "@/sampleAgentData/gallery";
import { helloSample } from "@/sampleAgentData/greetings";
import { hitlSample } from "@/sampleAgentData/hitl";
import { layoutSample } from "@/sampleAgentData/layout";
import { productSample } from "@/sampleAgentData/product";
import { profileSample } from "@/sampleAgentData/profile";
import { settingsSample } from "@/sampleAgentData/setting";
import { typographySample } from "@/sampleAgentData/typography";
import { SampleType } from "@/types/chat";

const deleteSurfaceAction = [
  {
    deleteSurface: {
      surfaceId: "temporary",
    },
  },
];

const samples: Record<SampleType, object[]> = {
  typography: typographySample,
  form: formSample,
  gallery: gallerySample,
  dashboard: dashboardSample,
  profile: profileSample,
  settings: settingsSample,
  hitl: hitlSample,
  product: productSample,
  layout: layoutSample,
  "delete-surface": deleteSurfaceSample,
  hello: helloSample,
};

export function detectSampleType(input: string): SampleType {
  const lower = input.toLowerCase();
  if (lower.includes("typography") || lower.includes("text"))
    return "typography";
  if (
    lower.includes("form") ||
    lower.includes("input") ||
    lower.includes("field")
  )
    return "form";
  if (lower.includes("gallery") || lower.includes("image")) return "gallery";
  if (lower.includes("dashboard") || lower.includes("stats"))
    return "dashboard";
  if (lower.includes("profile") || lower.includes("user")) return "profile";
  if (lower.includes("settings") || lower.includes("config")) return "settings";
  if (lower.includes("hitl") || lower.includes("approval")) return "hitl";
  if (lower.includes("product") || lower.includes("card")) return "product";
  if (lower.includes("layout") || lower.includes("grid")) return "layout";
  if (lower.includes("delete") || lower.includes("remove"))
    return "delete-surface";
  return "hello";
}

export function getMockMessage(type: SampleType): object[] {
  return samples[type] ?? helloSample;
}

export function getDeleteSurfaceAction(): object[] {
  return deleteSurfaceAction;
}

export type { SampleType };
