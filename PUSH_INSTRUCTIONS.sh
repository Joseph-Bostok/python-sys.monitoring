#!/bin/bash
# Instructions to push all branches to GitHub

echo "=========================================="
echo "GIT BRANCHES READY TO PUSH"
echo "=========================================="
echo ""

echo "Three branches have been created with all changes:"
echo ""

echo "1. cpython/per-call-statistics-tracking"
echo "   - Modified _lsprof.c source code"
echo "   - DO NOT push to official Python repo"
echo "   - Fork cpython first, then push to your fork"
echo ""

echo "2. python-sys.monitoring/per-call-statistics-implementation"
echo "   - Updated meeting_notes.txt"
echo "   - Ready to push to your repo"
echo ""

echo "3. cProfiler/per-call-statistics"
echo "   - All documentation and test files"
echo "   - Need to create new repo or update remote"
echo ""

echo "=========================================="
echo "QUICK PUSH (python-sys.monitoring only)"
echo "=========================================="
echo ""
echo "Run these commands to push the documentation updates:"
echo ""
echo "  cd /home/jbostok/cProfiler/python-sys.monitoring"
echo "  git push -u origin per-call-statistics-implementation"
echo ""

echo "=========================================="
echo "FULL SETUP (All repos)"
echo "=========================================="
echo ""
echo "See GIT_BRANCHES.md for complete instructions"
echo ""

# Show current branch status
echo "=========================================="
echo "CURRENT BRANCH STATUS"
echo "=========================================="
echo ""

echo "cpython:"
cd /home/jbostok/cProfiler/cpython
git branch | grep "*"
git log -1 --oneline

echo ""
echo "python-sys.monitoring:"
cd /home/jbostok/cProfiler/python-sys.monitoring
git branch | grep "*"
git log -1 --oneline

echo ""
echo "cProfiler (parent):"
cd /home/jbostok/cProfiler
git branch | grep "*"
git log -1 --oneline

echo ""
echo "=========================================="
echo "All changes committed locally!"
echo "See GIT_BRANCHES.md for push instructions"
echo "=========================================="
