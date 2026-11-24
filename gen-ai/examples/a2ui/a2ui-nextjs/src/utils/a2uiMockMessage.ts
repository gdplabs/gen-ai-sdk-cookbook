import { dashboardSample as dashboardSampleV08 } from "@/sampleAgentData/v0_8/dashboard";
import { deleteSurfaceSample as deleteSurfaceSampleV08 } from "@/sampleAgentData/v0_8/deleteSurface";
import { formSample as formSampleV08 } from "@/sampleAgentData/v0_8/form";
import { gallerySample as gallerySampleV08 } from "@/sampleAgentData/v0_8/gallery";
import { helloSample as helloSampleV08 } from "@/sampleAgentData/v0_8/greetings";
import { hitlSample as hitlSampleV08 } from "@/sampleAgentData/v0_8/hitl";
import { layoutSample as layoutSampleV08 } from "@/sampleAgentData/v0_8/layout";
import { productSample as productSampleV08 } from "@/sampleAgentData/v0_8/product";
import { profileSample as profileSampleV08 } from "@/sampleAgentData/v0_8/profile";
import { componentsSample as componentsSampleV08 } from "@/sampleAgentData/v0_8/components";
import { settingsSample as settingsSampleV08 } from "@/sampleAgentData/v0_8/setting";
import { typographySample as typographySampleV08 } from "@/sampleAgentData/v0_8/typography";

import { dashboardSample as dashboardSampleV09 } from "@/sampleAgentData/v0_9/dashboard";
import { deleteSurfaceSample as deleteSurfaceSampleV09 } from "@/sampleAgentData/v0_9/deleteSurface";
import { formSample as formSampleV09 } from "@/sampleAgentData/v0_9/form";
import { gallerySample as gallerySampleV09 } from "@/sampleAgentData/v0_9/gallery";
import { helloSample as helloSampleV09 } from "@/sampleAgentData/v0_9/greetings";
import { hitlSample as hitlSampleV09 } from "@/sampleAgentData/v0_9/hitl";
import { layoutSample as layoutSampleV09 } from "@/sampleAgentData/v0_9/layout";
import { productSample as productSampleV09 } from "@/sampleAgentData/v0_9/product";
import { profileSample as profileSampleV09 } from "@/sampleAgentData/v0_9/profile";
import { componentsSample as componentsSampleV09 } from "@/sampleAgentData/v0_9/components";
import { settingsSample as settingsSampleV09 } from "@/sampleAgentData/v0_9/setting";
import { typographySample as typographySampleV09 } from "@/sampleAgentData/v0_9/typography";

import { dashboardSample as dashboardSampleV10 } from "@/sampleAgentData/v1_0/dashboard";
import { deleteSurfaceSample as deleteSurfaceSampleV10 } from "@/sampleAgentData/v1_0/deleteSurface";
import { formSample as formSampleV10 } from "@/sampleAgentData/v1_0/form";
import { gallerySample as gallerySampleV10 } from "@/sampleAgentData/v1_0/gallery";
import { helloSample as helloSampleV10 } from "@/sampleAgentData/v1_0/greetings";
import { hitlSample as hitlSampleV10 } from "@/sampleAgentData/v1_0/hitl";
import { layoutSample as layoutSampleV10 } from "@/sampleAgentData/v1_0/layout";
import { productSample as productSampleV10 } from "@/sampleAgentData/v1_0/product";
import { profileSample as profileSampleV10 } from "@/sampleAgentData/v1_0/profile";
import { componentsSample as componentsSampleV10 } from "@/sampleAgentData/v1_0/components";
import { settingsSample as settingsSampleV10 } from "@/sampleAgentData/v1_0/setting";
import { typographySample as typographySampleV10 } from "@/sampleAgentData/v1_0/typography";

import { A2UIVersion, SampleType } from "@/types/chat";

const deleteSurfaceActionV08 = [
  {
    deleteSurface: {
      surfaceId: "temporary",
    },
  },
];

const deleteSurfaceActionV09 = [
  {
    version: "v0.9",
    deleteSurface: {
      surfaceId: "temporary",
    },
  },
];

const deleteSurfaceActionV10 = [
  {
    version: "1.0",
    deleteSurface: {
      surfaceId: "temporary",
    },
  },
];

const samplesV08: Record<SampleType, object[]> = {
  typography: typographySampleV08,
  form: formSampleV08,
  gallery: gallerySampleV08,
  dashboard: dashboardSampleV08,
  profile: profileSampleV08,
  settings: settingsSampleV08,
  hitl: hitlSampleV08,
  product: productSampleV08,
  layout: layoutSampleV08,
  "delete-surface": deleteSurfaceSampleV08,
  components: componentsSampleV08,
  hello: helloSampleV08,
};

const samplesV09: Record<SampleType, object[]> = {
  typography: typographySampleV09,
  form: formSampleV09,
  gallery: gallerySampleV09,
  dashboard: dashboardSampleV09,
  profile: profileSampleV09,
  settings: settingsSampleV09,
  hitl: hitlSampleV09,
  product: productSampleV09,
  layout: layoutSampleV09,
  "delete-surface": deleteSurfaceSampleV09,
  components: componentsSampleV09,
  hello: helloSampleV09,
};

const samplesV10: Record<SampleType, object[]> = {
  typography: typographySampleV10,
  form: formSampleV10,
  gallery: gallerySampleV10,
  dashboard: dashboardSampleV10,
  profile: profileSampleV10,
  settings: settingsSampleV10,
  hitl: hitlSampleV10,
  product: productSampleV10,
  layout: layoutSampleV10,
  "delete-surface": deleteSurfaceSampleV10,
  components: componentsSampleV10,
  hello: helloSampleV10,
};

const samplesByVersion: Record<A2UIVersion, Record<SampleType, object[]>> = {
  "0.8": samplesV08,
  "0.9": samplesV09,
  "1.0": samplesV10,
};

const deleteSurfaceActionByVersion: Record<A2UIVersion, object[]> = {
  "0.8": deleteSurfaceActionV08,
  "0.9": deleteSurfaceActionV09,
  "1.0": deleteSurfaceActionV10,
};

export function detectSampleType(input: string): SampleType {
  const lower = input.toLowerCase();
  if (lower.includes("typography") || lower.includes("text")) return "typography";
  if (lower.includes("form") || lower.includes("input") || lower.includes("field")) return "form";
  if (lower.includes("gallery") || lower.includes("image")) return "gallery";
  if (lower.includes("dashboard") || lower.includes("stats")) return "dashboard";
  if (lower.includes("profile") || lower.includes("user")) return "profile";
  if (lower.includes("settings") || lower.includes("config")) return "settings";
  if (lower.includes("hitl") || lower.includes("approval")) return "hitl";
  if (lower.includes("product") || lower.includes("card")) return "product";
  if (lower.includes("layout") || lower.includes("grid")) return "layout";
  if (lower.includes("delete") || lower.includes("remove")) return "delete-surface";
  if (lower.includes("components") || lower.includes("component") || lower.includes("catalog"))
    return "components";
  return "hello";
}

export function getMockMessage(type: SampleType, version: A2UIVersion): object[] {
  const samples = samplesByVersion[version];
  return samples[type] ?? samples.hello;
}

export function getDeleteSurfaceAction(version: A2UIVersion): object[] {
  return deleteSurfaceActionByVersion[version];
}

export type { SampleType };
