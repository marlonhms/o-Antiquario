import {
  type AtmosphereIntent,
  type ConsultationIntentV2,
  type OccasionPreset,
} from "./consultation-schema.ts";
import { DEFAULT_INTENT_V2, STORAGE_KEY_V2 } from "./migrate-v1-to-v2.ts";

export type ConsultationStep = "moment" | "atmosphere" | "results";

export interface ConsultationState {
  readonly step: ConsultationStep;
  readonly intent: ConsultationIntentV2;
  readonly isRefinementOpen: boolean;
  readonly isContextCorrectionOpen: boolean;
}

export type ConsultationAction =
  | { type: "SELECT_OCCASION"; occasion: OccasionPreset }
  | { type: "SELECT_ATMOSPHERE"; atmosphere: AtmosphereIntent }
  | { type: "SET_STEP"; step: ConsultationStep }
  | { type: "UPDATE_INTENT"; updates: Partial<ConsultationIntentV2> }
  | { type: "TOGGLE_HARD_AVOID_NOTE"; note: string }
  | { type: "TOGGLE_AVOIDED_ACCORD"; accord: string }
  | { type: "SET_CONTEXT_OVERRIDE"; overrides: NonNullable<ConsultationIntentV2["customContextOverrides"]> }
  | { type: "SET_REFINEMENT_OPEN"; isOpen: boolean }
  | { type: "SET_CONTEXT_CORRECTION_OPEN"; isOpen: boolean }
  | { type: "RESET_ALL" };

export function persistIntent(intent: ConsultationIntentV2): void {
  try {
    window.localStorage.setItem(STORAGE_KEY_V2, JSON.stringify(intent));
  } catch {
    // Falha silenciosa em navegadores com storage restrito
  }
}

export function consultationReducer(
  state: ConsultationState,
  action: ConsultationAction,
): ConsultationState {
  switch (action.type) {
    case "SELECT_OCCASION": {
      const nextIntent: ConsultationIntentV2 = {
        ...state.intent,
        occasion: action.occasion,
      };
      persistIntent(nextIntent);
      return {
        ...state,
        intent: nextIntent,
        step: "atmosphere",
      };
    }

    case "SELECT_ATMOSPHERE": {
      const nextIntent: ConsultationIntentV2 = {
        ...state.intent,
        atmosphere: action.atmosphere,
      };
      persistIntent(nextIntent);
      return {
        ...state,
        intent: nextIntent,
        step: "results",
      };
    }

    case "SET_STEP":
      return {
        ...state,
        step: action.step,
      };

    case "UPDATE_INTENT": {
      const nextIntent: ConsultationIntentV2 = {
        ...state.intent,
        ...action.updates,
      };
      persistIntent(nextIntent);
      return {
        ...state,
        intent: nextIntent,
      };
    }

    case "TOGGLE_HARD_AVOID_NOTE": {
      const exists = state.intent.hardAvoidNotes.includes(action.note);
      const hardAvoidNotes = exists
        ? state.intent.hardAvoidNotes.filter((n) => n !== action.note)
        : [...state.intent.hardAvoidNotes, action.note];
      const nextIntent: ConsultationIntentV2 = { ...state.intent, hardAvoidNotes };
      persistIntent(nextIntent);
      return { ...state, intent: nextIntent };
    }

    case "TOGGLE_AVOIDED_ACCORD": {
      const exists = state.intent.avoidedCanonicalIds.includes(action.accord);
      const avoidedCanonicalIds = exists
        ? state.intent.avoidedCanonicalIds.filter((a) => a !== action.accord)
        : [...state.intent.avoidedCanonicalIds, action.accord];
      const nextIntent: ConsultationIntentV2 = { ...state.intent, avoidedCanonicalIds };
      persistIntent(nextIntent);
      return { ...state, intent: nextIntent };
    }

    case "SET_CONTEXT_OVERRIDE": {
      const nextIntent: ConsultationIntentV2 = {
        ...state.intent,
        customContextOverrides: {
          ...state.intent.customContextOverrides,
          ...action.overrides,
        },
      };
      persistIntent(nextIntent);
      return {
        ...state,
        intent: nextIntent,
      };
    }

    case "SET_REFINEMENT_OPEN":
      return {
        ...state,
        isRefinementOpen: action.isOpen,
      };

    case "SET_CONTEXT_CORRECTION_OPEN":
      return {
        ...state,
        isContextCorrectionOpen: action.isOpen,
      };

    case "RESET_ALL": {
      try {
        window.localStorage.removeItem(STORAGE_KEY_V2);
      } catch {
        // Ignorar
      }
      return {
        step: "moment",
        intent: DEFAULT_INTENT_V2,
        isRefinementOpen: false,
        isContextCorrectionOpen: false,
      };
    }
  }
}
