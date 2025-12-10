"use client";

import { useState, useEffect, useCallback } from "react";
import { api, DashboardSummary, BreakdownItem, MetricTimeSeries, Alert, CampaignSummary, Account } from "./api";

// Hook for fetching dashboard summary
export function useDashboardSummary(dateRange?: { start: string; end: string }) {
    const [data, setData] = useState<DashboardSummary | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const summary = await api.getDashboardSummary(dateRange);
            setData(summary);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to fetch dashboard data - backend API not connected");
            // No mock fallback - show actual error
            setData(null);
        } finally {
            setIsLoading(false);
        }
    }, [dateRange?.start, dateRange?.end]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return { data, isLoading, error, refetch: fetchData };
}

// Hook for fetching metrics time series
export function useMetricsTimeSeries(
    metrics: string[],
    dateRange?: { start: string; end: string }
) {
    const [data, setData] = useState<MetricTimeSeries[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        if (metrics.length === 0) return;
        setIsLoading(true);
        setError(null);
        try {
            const timeSeries = await api.getMetricsTimeSeries(metrics, dateRange);
            setData(timeSeries);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to fetch metrics - backend API not connected");
            // No mock fallback
            setData([]);
        } finally {
            setIsLoading(false);
        }
    }, [metrics.join(","), dateRange?.start, dateRange?.end]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return { data, isLoading, error, refetch: fetchData };
}

// Hook for fetching campaign breakdown
export function useCampaignBreakdown(dateRange?: { start: string; end: string }) {
    const [data, setData] = useState<BreakdownItem[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.getBreakdown("campaign", dateRange);
            setData(response.items);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to fetch campaigns - backend API not connected");
            setData([]);
        } finally {
            setIsLoading(false);
        }
    }, [dateRange?.start, dateRange?.end]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    return { data, isLoading, error, refetch: fetchData };
}

// Hook for fetching alerts
export function useAlerts(filters?: { severity?: string; is_read?: boolean }) {
    const [data, setData] = useState<Alert[]>([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.getAlerts(filters);
            setData(response.alerts);
            setUnreadCount(response.unread_count);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to fetch alerts - backend API not connected");
            setData([]);
            setUnreadCount(0);
        } finally {
            setIsLoading(false);
        }
    }, [filters?.severity, filters?.is_read]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const markAsRead = async (alertId: string) => {
        try {
            await api.markAlertRead(alertId);
            setData(prev => prev.map(a => a.id === alertId ? { ...a, is_read: true } : a));
            setUnreadCount(prev => Math.max(0, prev - 1));
        } catch {
            // Optimistic update even on error for demo
            setData(prev => prev.map(a => a.id === alertId ? { ...a, is_read: true } : a));
            setUnreadCount(prev => Math.max(0, prev - 1));
        }
    };

    const markAllAsRead = async () => {
        try {
            await api.markAllAlertsRead();
            setData(prev => prev.map(a => ({ ...a, is_read: true })));
            setUnreadCount(0);
        } catch {
            setData(prev => prev.map(a => ({ ...a, is_read: true })));
            setUnreadCount(0);
        }
    };

    return { data, unreadCount, isLoading, error, refetch: fetchData, markAsRead, markAllAsRead };
}

// Hook for fetching accounts
export function useAccounts() {
    const [data, setData] = useState<Account[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await api.getAccounts();
            setData(response.accounts);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to fetch accounts");
            setData([]);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const triggerSync = async (accountId: string, fullSync = false) => {
        try {
            await api.triggerSync(accountId, fullSync);
            return true;
        } catch {
            return false;
        }
    };

    return { data, isLoading, error, refetch: fetchData, triggerSync };
}

// Note: Mock data generators removed - backend API required for dashboard, alerts, metrics data
// Partner APIs (Kelkoo, Admedia, MaxBounty) work independently via useKelkooData, useAdmediaData, useMaxBountyData hooks
