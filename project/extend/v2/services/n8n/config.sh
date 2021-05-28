#!/usr/bin/env bash

n8nConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=n8n"
  echo "\nN8N_VERSION="${N8N_VERSION}
}
