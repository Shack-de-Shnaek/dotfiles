#!/bin/sh
niri msg action focus-monitor-left &
niri msg action move-workspace-to-monitor-right &
niri msg action focus-monitor-right &
niri msg action focus-workspace-up &
niri msg action move-workspace-to-monitor-left &
niri msg action focus-monitor-left
