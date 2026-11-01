/**
 * NexAbility Candidate API Service
 * Manages candidate profile and optional disability self-declaration
 * according to the NexAbility API Contract.
 */

import { apiClient } from "./client.js";

export const candidateService = {
  /**
   * Save voluntary disability declaration
   * Endpoint: PUT /candidates/me/declaration
   * Request body: { accepted: true, declaration_version: "v1" }
   * Note: The declaration is strictly voluntary. Never send accepted: false to withdraw.
   */
  async saveDeclaration({ accepted = true, declaration_version = "v1" } = {}) {
    return apiClient.put(
      "/candidates/me/declaration",
      { accepted, declaration_version },
      { requiresAuth: true }
    );
  },

  /**
   * Retrieve current disability declaration status
   * Endpoint: GET /candidates/me/declaration
   */
  async getDeclaration() {
    return apiClient.get("/candidates/me/declaration", { requiresAuth: true });
  },

  /**
   * Withdraw voluntary disability declaration
   * Endpoint: DELETE /candidates/me/declaration
   * Note: Withdrawing deletes the declaration. It does not send accepted: false.
   */
  async withdrawDeclaration() {
    return apiClient.delete("/candidates/me/declaration", { requiresAuth: true });
  },
};

export default candidateService;
